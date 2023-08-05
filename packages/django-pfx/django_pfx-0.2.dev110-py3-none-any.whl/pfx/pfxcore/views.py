import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey, Manager, Model
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views import View

from django_request_mapping import request_mapping

from .exceptions import APIError, ModelNotFoundAPIError
from .shortcuts import f

logger = logging.getLogger(__name__)


LIST_META = ['count', 'pagination']


def parse_list_meta(request):
    meta_arg = request.GET.get('meta', 'all')
    meta = meta_arg.split(',') or []
    if 'all' in meta:
        return LIST_META
    return meta


def pfx_api():
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.request = request
            self.kwargs = kwargs
            try:
                return func(self, request, *args, **kwargs)
            except APIError as e:
                return e.response
            except Exception as e:
                logger.exception(e)
                return JsonResponse(dict(message=str(e)), status=500)
        return wrapper
    return decorator


def rest_api(*dec_args, **dec_kwargs):
    _request_mapping = request_mapping(*dec_args, **dec_kwargs)
    _pfx_api = pfx_api()

    def decorator(func):
        return _request_mapping(_pfx_api(func))
    return decorator


rest_view = request_mapping


class ModelMixin:
    queryset = None
    fields = []

    def get_queryset(self):
        return self.queryset

    def get_fields(self):
        return self.fields or [f.name for f in self.model._meta.fields]

    @property
    def model(self):
        return self.get_queryset().model

    @property
    def model_name(self):
        return self.model._meta.verbose_name

    def _json_object(self, obj):
        return dict(pk=obj.pk, resource_name=str(obj))

    def message_response(self, message, **kwargs):
        return JsonResponse(dict(message=message, **kwargs))


class ModelResponseMixin(ModelMixin):
    def serialize_field(self, obj, field):
        value = getattr(obj, field)
        if isinstance(value, Model):
            return self._json_object(value)
        elif isinstance(value, Manager):
            return [self._json_object(o) for o in value.all()]
        return value

    def serialize_object(self, obj, **fields):
        return dict(**self._json_object(obj), **fields)

    def response(self, o, **meta):
        return JsonResponse(self.serialize_object(o, **{
            f: self.serialize_field(o, f)
            for f in self.get_fields()}, meta=meta))


class BodyMixin:
    def deserialize_body(self, request):
        return json.loads(request.body)


class ModelBodyMixin(BodyMixin, ModelMixin):
    readonly_fields = []

    def get_readonly_fields(self):
        return self.readonly_fields

    def _field_data(self, field_name, value):
        field = self.model._meta.get_field(field_name)
        if isinstance(field, ForeignKey):
            model = field.related_model
            try:
                return field_name, model.objects.get(pk=value)
            except ObjectDoesNotExist:
                raise ModelNotFoundAPIError(model)
        return field_name, value

    def get_model_data(self, request):
        data = self.deserialize_body(request)
        data.pop('id', None)
        data.pop('pk', None)
        return dict(
            self._field_data(k, v) for k, v in data.items()
            # Todo: throw an error for non existing fields.
            if k in self.get_fields() and
            # Todo: Log a warning for readonly ignores fields.
            k not in self.get_readonly_fields())


class ListRestViewMixin(ModelResponseMixin):
    list_fields = []

    def get_list_fields(self):
        return self.list_fields or self.get_fields()

    def _list_meta_count(self, request):
        return self.get_queryset().count()

    def _list_meta_pagination(self, request):
        return dict(
            page_size=int(request.GET.get('page_size', 10)),
            page=int(request.GET.get('page', 1)),
            page_subset=int(request.GET.get('page_subset', 5)))

    def build_list_meta(self, request):
        return {
            meta: getattr(self, f'_list_meta_{meta}')(request)
            for meta in parse_list_meta(request)}

    def get_queryset(self):
        return super().get_queryset()

    def get_list_result(self, qs):
        for o in qs:
            yield self.serialize_object(o, **{
                f: self.serialize_field(o, f)
                for f in self.get_list_fields()})

    @rest_api("", method="get")
    def get_list(self, request, *args, **kwargs):
        res = {}
        meta = self.build_list_meta(request)
        qs = self.get_queryset()
        if 'pagination' in meta:
            count = qs.count()
            pagination = meta['pagination']
            page = pagination['page']
            limit = pagination['page_size']
            page_count = 1 + (count - 1) // limit
            offset = (page - 1) * limit
            subset = pagination['page_subset']
            subset_first = min(
                max(page - subset // 2, 1), max(page_count - subset + 1, 1))
            qs = qs.all()[offset:offset+limit]
            pagination.update(dict(
                count=count,
                page_count=page_count,
                subset=list(range(
                    subset_first,
                    min(subset_first + subset, page_count + 1)))))
        else:
            qs = qs.all()
        if meta:
            res['meta'] = meta
        res['items'] = list(self.get_list_result(qs))
        return JsonResponse(res)


class DetailRestViewMixin(ModelResponseMixin):
    @rest_api("/<int:id>", method="get")
    def get(self, request, id, *args, **kwargs):
        qs = self.get_queryset().filter(id=id)
        if qs:
            return self.response(qs[0])
        raise ModelNotFoundAPIError(self.model)


class CreateRestViewMixin(ModelBodyMixin, ModelResponseMixin):
    @rest_api("", method="post")
    def post(self, request, *args, **kwargs):
        data = self.get_model_data(request)
        obj = self.get_queryset().create(**data)
        return self.response(
            obj, message=f(
                _("{model} {obj} created."), model=self.model_name, obj=obj))


class UpdateRestViewMixin(ModelBodyMixin):
    @rest_api("/<int:id>", method="put")
    def put(self, request, id, *args, **kwargs):
        data = self.get_model_data(request)
        qs = self.get_queryset().filter(pk=id)
        if qs.exists():
            qs.update(**data)
            obj = qs.first()
            return self.response(
                obj, message=f(
                    _("{model} {obj} updated."),
                    model=self.model_name, obj=obj))
        raise ModelNotFoundAPIError(self.model)


class DeleteRestViewMixin(ModelMixin):
    @rest_api("/<int:id>", method="delete")
    def delete(self, request, id, *args, **kwargs):
        try:
            obj = self.get_queryset().get(pk=id)
            obj.delete()
            return self.message_response(f(
                _("{model} {obj} deleted."), model=self.model_name, obj=obj))
        except self.model.DoesNotExist:
            raise ModelNotFoundAPIError(self.model)


class BaseRestView(View):
    pass


class RestView(
        ListRestViewMixin,
        DetailRestViewMixin,
        CreateRestViewMixin,
        UpdateRestViewMixin,
        DeleteRestViewMixin,
        BaseRestView):
    pass
