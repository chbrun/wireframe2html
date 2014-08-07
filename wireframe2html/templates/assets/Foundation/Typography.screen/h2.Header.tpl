<h2>
{% if ref_5 is defined %}
    {% set title =  ref_5.text | get_title_data %}
        {{ title.text|default('Header') }} 
        {% if title.small is defined %}
            <small style="font-size:{{ title.small.font }}px">
                {{ title.small.text }}
            </small>
        {% endif %}
{% else %}
    Header
{% endif %}
</h2>
