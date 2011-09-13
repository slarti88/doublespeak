#DoubleSpeakMain will change your life
from django.utils import simplejson

from google.appengine.ext.webapp import util

import os
import Models

import fix_path
from tornado import wsgi, web, template

def error(msg):
    err = dict()
    err['message'] = msg
    return err


class TopicsHandler(web.RequestHandler):
    def get(self):
        topics = Models.Topic.all()
        topicsDict = []
        for topic in topics:
            topicDict = topic.marshal()
            if topicDict:
                topicsDict.append(topicDict)
        self.write(simplejson.dumps(topicsDict))

    def post(self):
        if self.request.body:
            topic = Models.Topic()
            topic.unmarshal(simplejson.loads(self.request.body))
            topic.persist()


class TopicHandler(web.RequestHandler):
    def get(self, topic_id):
        topic = Models.Topic.get_by_id(int(topic_id))
        if topic:
            self.write(simplejson.dumps(topic.marshal()))
        else:
            self.write(error('Topic not found.'))

    def put(self, topic_id):
        if self.request.body:
            topic = Models.Topic.get_by_id(int(topic_id))
            topic.unmarshal(simplejson.loads(self.request.body))
            topic.persist()


class TopicLinksHandler(web.RequestHandler):
    def get(self, topic_id):
        topic = Models.Topic.get_by_id(int(topic_id))
        if topic:
            topicDict = topic.marshal()
            self.write(simplejson.dumps(topicDict['links']))
        else:
            self.write(error('Topic not found.'))

    def post(self, topic_id):
        if self.request.body:
            topic = Models.Topic.get_by_id(int(topic_id))
            topicDict = dict()
            topicDict['links'] = []
            topicDict['links'].append(simplejson.loads(self.request.body))
            topic.unmarshal(topicDict)
            topic.persist()


class TopicLinkHandler(web.RequestHandler):
    def get(self, topic_id, link_id):
        link = Models.Link.get_by_id(int(link_id))
        if link:
            self.write(simplejson.dumps(link.marshal()))
        else:
            self.write(error('Link not found.'))

    def put(self, topic_id, link_id): #vote up/down information will be stored in the TopicLink table.
        if self.request.body:
            link = Models.Link.get_by_id(int(link_id))
            link.unmarshal(simplejson.loads(self.request.body))
            link.persist()

class FrontMainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello world!")

class FrontTopicHandler(web.RequestHandler):
    def get(self, topic_id):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)
    
settings = {
    "page_title": u"doubleSpeak",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "sourcecode_stylesheet": "default",
    "xsrf_cookies": False,
    }

handlers = [
    (r"/", FrontMainHandler),
    (r"/topics/(\d+)", FrontTopicHandler),
    (r"/api/topics", TopicsHandler),
    (r"/api/topics/(\d+)", TopicHandler),
    (r"/api/topics/(\d+)/links", TopicLinksHandler),
    (r"/api/topics/(\d+)/links/(\d+)", TopicLinkHandler),
]

def main():
    application = wsgi.WSGIApplication(handlers, **settings)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()