<h1>
{% if ref_2 is defined %}
    {% set title =  ref_2.text | get_title_data %}
        {{ title.text|default('Header') }} 
        {% if title.small is defined %}
            <small style="font-size:{{ title.small.font }}px">
                {{ title.small.text }}
            </small>
        {% endif %}
{% else %}
    Header
{% endif %}
</h1>
