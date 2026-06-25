from flask import Blueprint, render_template, request, redirect, flash

bp_forgot_password=Blueprint("forgot_password", __name__)


@bp_forgot_password.route("/forgot_password")
def forgot_password():

	return render_template("forgot_password.html")