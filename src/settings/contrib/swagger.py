from ..environment import env


SWAGGER_SETTINGS = {
    "DEFAULT_API_URL": env.str("SRC_BASE_API_URL", default="https://example.com"),
}
