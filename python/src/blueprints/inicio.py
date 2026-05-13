from flask import Blueprint, render_template

bp_inicio=Blueprint("inicio", __name__)


@bp_inicio.route("/")
def inicio():

	return render_template("inicio.html")

@bp_inicio.route('/health')
def health():
	
    return "OK", 200