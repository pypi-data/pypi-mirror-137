def render_string_template(template,config):
    from jinja2 import Environment
    env=Environment()
    return env.from_string(template).render(**config)