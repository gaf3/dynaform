"""
Module for the OPenGUI API
"""

# pylint: disable=no-self-use

import flask
import flask_restful

import opengui

def build():
    """
    Builds the Flask App
    """

    app = flask.Flask("opengui-api")
    api = flask_restful.Api(app)

    api.add_resource(Health, '/health')
    api.add_resource(Example, '/example')


    return app


class Health(flask_restful.Resource):
    """
    Class for Health checks
    """

    def get(self):
        """
        Just return ok
        """
        return {"message": "OK"}


class Example(flask_restful.Resource):
    """
    Class with examples
    """

    def fields(self, values):
        """
        This builds the fields object dynamically
        """

        # Create a single multi select field

        fields = opengui.Fields(
            values=values,
            fields=[
                {
                    "name": "types",
                    "options": [
                        "textarea",
                        "options",
                        "fields"
                    ],
                    "multi": True,
                    "trigger": True
                }
            ]
        )

        # If they select textarea, add it

        if "textarea" in (fields["types"].value or []):
            fields.append({
                "name": "people",
                "style": "textarea"
            })
            fields.ready = True

        # If they selected option, add a format, then check what format they selected

        if "options" in (fields["types"].value or []):
            fields.append({
                "name": "style",
                "options": [
                    "radios",
                    "select"
                ],
                "default": "radios",
                "trigger": True
            })
            fields.append({
                "name": "stuff",
                "options": [
                    "fee",
                    "fie",
                    "foe",
                    "fum"
                ],
                "style": fields["style"].value
            })
            fields.ready = True

        # If they add subfields, add two, and make the second optional

        if "fields" in (fields["types"].value or []):
            fields.append({
                "name": "things",
                "fields": [
                    {
                        "name": "yin",
                    },
                    {
                        "name": "yang",
                        "optional": True
                    }
                ]
            })
            fields.ready = True

        return fields

    def options(self):
        """
        We use the options endpoints for showing what the field options are
        This is the endpoint used to go back and forth
        """

        fields = self.fields((flask.request.json or {}).get("values"))

        fields.validate()

        return fields.to_dict(), 200

    def post(self):
        """
        This is the endpoint to actual submit data
        """

        values = (flask.request.json or {}).get("values")

        fields = self.fields(values)

        if not fields.validate():
            return fields.to_dict(), 400

        return {"message": "created", "values": values}, 201
