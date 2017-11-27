from flask import Flask
from flask import render_template_string
from flask_menu import Menu, register_menu
from flask import Blueprint
from flask_menu.classy import register_flaskview
from flask_classy import FlaskView
from flask_menu.classy import classy_menu_item

app = Flask(__name__)


class MyEndpoint(FlaskView):
    route_base = '/'

    @classy_menu_item('index', 'Home', order=0)
    def index(self):
        # Do something.
        return render_template_string(
        """
        <ul>
  {%- for item in current_menu.children recursive -%}
  <li>
    <a href="{{ item.url}}">{{ item.text }}</a>
    {%- if item.children -%}
    <ul>
      {{ loop(item.children) }}
    </ul>
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
        """)

    @classy_menu_item('index2', 'Home2', order=1)
    def index2(self):
        # Do something.
        return render_template_string(
        """
        <ul>
  {%- for item in current_menu.children recursive -%}
  <li>
    <a href="{{ item.url}}">{{ item.text }}</a>
    {%- if item.children -%}
    <ul>
      {{ loop(item.children) }}
    </ul>
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
        """)

bp = Blueprint('bp', __name__)
# MyEndpoint.register(app)
MyEndpoint.register(bp)
register_flaskview(bp, MyEndpoint)
Menu(app=app)
app.register_blueprint(bp)


def tmpl_show_menu():
    return render_template_string(
        """
        <ul>
  {%- for item in current_menu.children recursive -%}
  <li>
    <a href="{{ item.url}}">{{ item.text }}</a>
    {%- if item.children -%}
    <ul>
      {{ loop(item.children) }}
    </ul>
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
        """)

@app.route('/sdfsdfsdf')
@register_menu(app, '.', 'Home')
def index():

    return tmpl_show_menu()

@app.route('/first')
@register_menu(app, '.first', 'First', order=2)
def first():
    return tmpl_show_menu()

@app.route('/second')
@register_menu(app, '.second', 'Second', order=3)
def second():
    return tmpl_show_menu()

bp_account = Blueprint('.', __name__, url_prefix='/')
app.register_blueprint(bp_account)

@bp_account.route('/')
@register_menu(bp_account, '.account', 'Your account')
def index():
    pass










if __name__ == '__main__':
    app.run(debug=True)