_CONTENT = {
	'login.html': """{% raw %}<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Authentication</title>
	<style>
		body { margin: 2em auto; max-width: 20em }
		input[type=submit] { width: 100%; margin-top: 1em }
	</style>
</head>
<body>
	{% block content %}

		{% if form.errors %}
			<p style="color:darkred">Your username and password didn't match. Please try again.</p>
		{% endif %}

		{% if next %}
			{% if user.is_authenticated %}
				<p>Your account doesn't have access to this page. To proceed, please login with an account that has access.</p>
			{% else %}
				<p>Please login to see this page.</p>
			{% endif %}
		{% endif %}

		<form method="post" action="{% url 'login' %}">
			{% csrf_token %}
		<table>

		<tr>
			<td>{{ form.username.label_tag }}</td>
			<td>{{ form.username }}</td>
		</tr>

		<tr>
			<td>{{ form.password.label_tag }}</td>
			<td>{{ form.password }}</td>
		</tr>
		</table>

		<input type="submit" value="Log in" />
		<input type="hidden" name="next" value="{{ next }}" />
		</form>

		{# Assumes you setup the password_reset view in your URLconf #}
		{# <p><a href="{% url 'password_reset' %}">Lost password?</a></p> #}

	{% endblock content %}
</body>
</html>
{% endraw %}""",

	'logged_out.html': """{% raw %}<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Logged out</title>
</head>
<body>
	<p>You have been successfully logged out.</p>
</body>
</html>
{% endraw %}""",
}
