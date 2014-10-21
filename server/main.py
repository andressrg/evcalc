import os
import webapp2
from webapp2_extras.routes import RedirectRoute
from google.appengine.ext.webapp import template

cdn_url = "http://scoremat-markup.appspot.com"


class PagesHandler(webapp2.RequestHandler):

    def get(self, template_path):
        path = os.path.join(os.path.dirname(__file__), 'pages/%s.html' % template_path)
        self.response.out.write(template.render(path, {
                                'cdn_url': cdn_url
                                }))


class MailHandler(webapp2.RequestHandler):

    def get(self, template_path):
        path = os.path.join(os.path.dirname(__file__), 'pages/mail_send.html')
        self.response.out.write(template.render(path, {
                                'mail_tempate': template_path
                                }))

    def post(self, template_path):
        from google.appengine.api import mail

        email_address = self.request.POST.get('email')
        mail_path = os.path.join(os.path.dirname(__file__), 'pages/%s.html' % template_path)

        message = mail.EmailMessage(sender='andres.srg@gmail.com',
                                    subject='Mail: %s test' % template_path, to=email_address)
        message.html = template.render(mail_path, {
                                       'cdn_url': cdn_url
                                       })
        message.send()

        page_path = os.path.join(os.path.dirname(__file__), 'pages/mail_send.html')

        self.response.out.write(template.render(page_path, {
                                'mail_tempate': template_path,
                                'mail_sent': True
                                }))


app = webapp2.WSGIApplication([
    RedirectRoute('/pages/<template_path>', PagesHandler, name='pages', strict_slash=True),
    RedirectRoute('/mail/<template_path>', MailHandler, name='mail', strict_slash=True)
], debug=True)
