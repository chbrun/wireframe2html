<h6>
{% if ref_13 is defined %}
    {% set title =  ref_13.text | get_title_data %}
        {{ title.text|default('Header') }} 
        {% if title.small is defined %}
            <small style="font-size:{{ title.small.font }}px">
                {{ title.small.text }}
            </small>
        {% endif %}
{% else %}
    Header
{% endif %}
</h6>
