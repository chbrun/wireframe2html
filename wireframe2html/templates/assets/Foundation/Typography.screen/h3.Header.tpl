<h3>
{% if ref_7 is defined %}
    {% set title =  ref_7.text | get_title_data %}
        {{ title.text|default('Header') }} 
        {% if title.small is defined %}
            <small style="font-size:{{ title.small.font }}px">
                {{ title.small.text }}
            </small>
        {% endif %}
{% else %}
    Header
{% endif %}
</h3>
