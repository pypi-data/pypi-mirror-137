# Copyright (C) 2022 Jorge L. Juarez (https://github.com/JorgeJuarezM)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http


class HealthCheckController(http.Controller):
    @http.route("/healthcheck", methods=["GET"], type="json", auth="none")
    def healthcheck(self, **kwargs):
        return str(kwargs)
