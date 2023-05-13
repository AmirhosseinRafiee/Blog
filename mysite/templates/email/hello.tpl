{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}
This is an <strong>html</strong> part.
<a href=http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}>
http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}
</a>
{% endblock %}