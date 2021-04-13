from plone import api
from Products.Five import BrowserView
import json, logging

logger = logging.getLogger("Plone")

class Exporter(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
    
        with api.env.adopt_roles(roles=['Manager']):
        
            # Folders one lvl deep
            if self.request.form.get('folder','0') == '1':
                data = self.get_object_data(self.context) # get folder data
            
                all_data = []
                for brain in self.context.getFolderContents():
                    if self.request.form.get('ignore_folderish','0') == '0':
                        all_data.append(self.get_object_data(brain.getObject(), brain))
                    elif not brain.is_folderish:
                        all_data.append(self.get_object_data(brain.getObject(), brain))
                    
                data['__content'] = all_data
                
                return json.dumps(data, indent=4, sort_keys=True)
                
                
            # Single object
            return json.dumps(self.get_object_data(self.context), indent=4, sort_keys=True)
        
    
    def get_object_data(self, obj, brain=None):
    
        data = {}
        if not brain:
            brain = api.content.find(obj)[0]
        
        # PLONE NATIVE -----------------------------------
        data['portal_type'] = obj.portal_type
        data['getId'] = obj.getId()
        data['title'] = obj.title
        
        if brain.review_state:
            data['review_state'] = brain.review_state
        else:
            data['review_state'] = ""
        
        if hasattr(obj, 'description') and obj.description:
            data['description'] = obj.description
            
        if hasattr(obj, 'exclude_from_nav'):
            data['exclude_from_nav'] = obj.exclude_from_nav
        
        if hasattr(obj, 'body') and obj.body and hasattr(obj.body, 'output'):
            data['body'] = obj.body.output
            
        if hasattr(obj, 'text') and obj.text and hasattr(obj.text, 'output'):
            data['text'] = obj.text.output
            
        if hasattr(obj, 'getRemoteUrl') and obj.getRemoteUrl:
            data['getRemoteUrl'] = obj.getRemoteUrl
        
        if hasattr(obj, 'start') and obj.start:
            data['start'] = obj.start.strftime("%Y-%m-%d, %H:%M")
        
        if hasattr(obj, 'end') and obj.end:
            data['end'] = obj.end.strftime("%Y-%m-%d, %H:%M")
        
        if hasattr(obj, 'location') and obj.location:
            data['location'] = obj.location
        
        if hasattr(obj, 'Subject') and obj.Subject:
            data['Subject'] = obj.Subject()
        
            
        # To Base64 ------------------------------------------
        
        if hasattr(obj, 'image') and obj.image:
            data['image'] = self.to_base64(obj.image.data, 'BLOB:')
            data['filename'] = obj.image.filename
            
        if hasattr(obj, 'file') and obj.file:
            data['file'] = self.to_base64(obj.file.data, 'BLOB:')
            data['filename'] = obj.file.filename
        
        if hasattr(obj, 'json_data') and obj.json_data:
            data['json_data'] = self.to_base64(obj.json_data, 'JSON:')
        
        
        # UWO CUSTOM -------------------------------------
        
        if hasattr(obj, 'resources') and obj.resources:
            data['resources'] = obj.resources
        
        if hasattr(obj, 'campus') and obj.campus:
            data['campus'] = obj.campus
        
        if hasattr(obj, 'state') and obj.state:
            data['state'] = obj.state
        
        if hasattr(obj, 'email') and obj.email:
            data['email'] = obj.email
        
        if hasattr(obj, 'fax') and obj.fax:
            data['fax'] = obj.fax
        
        if hasattr(obj, 'disciplines') and obj.disciplines:
            data['disciplines'] = obj.disciplines
        
        if hasattr(obj, 'phone') and obj.phone:
            data['phone'] = obj.phone
        
        if hasattr(obj, 'supervisors') and obj.supervisors:
            data['supervisors'] = obj.supervisors
        
        if hasattr(obj, 'department') and obj.department:
            data['department'] = obj.department
        
        if hasattr(obj, 'funded') and obj.funded:
            data['funded'] = obj.funded
        
        if hasattr(obj, 'timeoff') and obj.timeoff:
            data['timeoff'] = obj.timeoff
        
        if hasattr(obj, 'position') and obj.position:
            data['position'] = obj.position
            
        if hasattr(obj, 'activated') and obj.activated:
            data['activated'] = obj.activated
            
        if hasattr(obj, 'academic_staff') and obj.academic_staff:
            data['academic_staff'] = obj.academic_staff
            
        if hasattr(obj, 'coverage') and obj.coverage:
            data['coverage'] = obj.coverage
            
        if hasattr(obj, 'workflow_status') and obj.workflow_status:
            data['workflow_status'] = obj.workflow_status
            
        if hasattr(obj, 'banned') and obj.banned:
            data['banned'] = obj.banned
            
        if hasattr(obj, 'banned_words') and obj.banned_words:
            data['banned_words'] = obj.banned_words
            
        if hasattr(obj, 'restrictions') and obj.restrictions:
            data['restrictions'] = obj.restrictions
            
        if hasattr(obj, 'extra_css') and obj.extra_css:
            data['extra_css'] = obj.extra_css
            
        if hasattr(obj, 'html') and obj.html:
            data['html'] = obj.html
            
        if hasattr(obj, 'css') and obj.css:
            data['css'] = obj.css
            
        if hasattr(obj, 'js') and obj.js:
            data['js'] = obj.js
            
        if hasattr(obj, 'subject_headings') and obj.subject_headings:
            data['subject_headings'] = obj.subject_headings
        
        if hasattr(obj, 'professional_background') and obj.professional_background and hasattr(obj.professional_background, 'output'):
            data['professional_background'] = obj.professional_background.output
            
        if hasattr(obj, 'community_involvment') and obj.community_involvment and hasattr(obj.community_involvment, 'output'):
            data['community_involvment'] = obj.community_involvment.output
            
        if hasattr(obj, 'education') and obj.education and hasattr(obj.education, 'output'):
            data['education'] = obj.education.output
            
        if hasattr(obj, 'prebody') and obj.prebody and hasattr(obj.prebody, 'output'):
            data['prebody'] = obj.prebody.output
            
        if hasattr(obj, 'message') and obj.message and hasattr(obj.message, 'output'):
            data['message'] = obj.message.output
            
        if hasattr(obj, 'libchat') and obj.libchat:
            data['libchat'] = obj.libchat
            
        if hasattr(obj, 'suppress_title'):
            data['suppress_title'] = obj.suppress_title
            
        if hasattr(obj, 'suppress_description'):
            data['suppress_description'] = obj.suppress_description
            
        if hasattr(obj, 'set_context') and obj.set_context:
            data['set_context'] = obj.set_context
            
        return data
        
    
    def to_base64(self, data, header):
        return header + data.encode('base64')
    
    
    
    @property
    def portal(self):
        return api.portal.get()