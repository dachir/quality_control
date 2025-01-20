app_name = "quality_control"
app_title = "Quality Control"
app_publisher = "Kossivi Dodzi Amouzou"
app_description = "This is custom module to manage quality control"
app_email = "dodziamouzou@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "quality_control",
# 		"logo": "/assets/quality_control/logo.png",
# 		"title": "Quality Control",
# 		"route": "/quality_control",
# 		"has_permission": "quality_control.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/quality_control/css/quality_control.css"
# app_include_js = "/assets/quality_control/js/quality_control.js"

# include js, css files in header of web template
# web_include_css = "/assets/quality_control/css/quality_control.css"
# web_include_js = "/assets/quality_control/js/quality_control.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "quality_control/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "quality_control/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "quality_control.utils.jinja_methods",
# 	"filters": "quality_control.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "quality_control.install.before_install"
# after_install = "quality_control.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "quality_control.uninstall.before_uninstall"
# after_uninstall = "quality_control.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "quality_control.utils.before_app_install"
# after_app_install = "quality_control.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "quality_control.utils.before_app_uninstall"
# after_app_uninstall = "quality_control.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "quality_control.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Item": "quality_control.overrides.item.CustomItem",
 	"Quality Inspection": "quality_control.overrides.quality_inspection.CustomQualityInspection",
    #"Purchase Receipt": "quality_control.overrides.purchase_receipt.CustomPurchaseReceipt",
    #"Stock Entry": "quality_control.overrides.stock_entry.CustomStockEntry",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"quality_control.tasks.all"
# 	],
# 	"daily": [
# 		"quality_control.tasks.daily"
# 	],
# 	"hourly": [
# 		"quality_control.tasks.hourly"
# 	],
# 	"weekly": [
# 		"quality_control.tasks.weekly"
# 	],
# 	"monthly": [
# 		"quality_control.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "quality_control.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "quality_control.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "quality_control.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["quality_control.utils.before_request"]
# after_request = ["quality_control.utils.after_request"]

# Job Events
# ----------
# before_job = ["quality_control.utils.before_job"]
# after_job = ["quality_control.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"quality_control.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Quality Control"]]},
    {"dt": "Client Script", "filters": [["enabled", "=", 1],["module", "=", "Quality Control"]]},
    {"dt": "Server Script", "filters": [["disabled", "=", 0],["module", "=", "Quality Control"]]},
]