from google.appengine.ext import webapp

from django.utils import simplejson as json

from model import Query, TemplateMetric
from lthandler import LTHandler

class InitTemplatesHandler(LTHandler):
  def get(self):
    user = self.get_user()
    if not user:
      return

    if TemplateMetric.all().count() > 0:
      return

    f = open('scripts/templates.json')
    json_templates = json.loads(f.read())

    for json_template in json_templates:
      template = TemplateMetric(
        format = json_template['format'],
        frequency = json_template['frequency'],
        name = json_template['name'],
        normalized_name = Query.normalize_name(json_template['name']),
        text = json_template['text'],
      )

      template.put()
      
    
