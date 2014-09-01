    <ul class="pricing-table">
      <li class="title">{{ ref_26.text | get_pricing_title }}</li>
      <li class="price">{{ ref_26.text | get_pricing_price }}</li>
      <li class="description">{{ ref_26.text | get_pricing_description }}</li>
        {% for value in ref_26.text | get_pricing_items %}
      <li class="bullet-item">{{ value }}</li>
        {% endfor %}
      <li class="cta-button"><a class="button radius {% if attr_state is defined %}disabled{% endif %}" {% if attr_background is defined %}style="background-color: {{ attr_background }};" {% endif %}href="#">{{ ref_29.text or 'Buy Now' }} </a></li>
    </ul>
