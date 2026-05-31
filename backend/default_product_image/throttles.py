from rest_framework.throttling import SimpleRateThrottle


class DefaultProductImageGenerationThrottle(SimpleRateThrottle):
    scope = "default_product_image_generation"
    rate = "10/min"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": request.user.pk,
        }
