from rest_framework.routers import SimpleRouter, DefaultRouter, Route, DynamicDetailRoute, DynamicListRoute

class CustomRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={
                'post': 'create'
            },
            name='{basename}-create',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/update{trailing_slash}$',
            mapping={
                'put': 'update',
                'patch': 'partial_update'
            },
            name='{basename}-update',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/destroy{trailing_slash}$',
            mapping={
                'delete': 'destroy'
            },
            name='{basename}-destroy',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
