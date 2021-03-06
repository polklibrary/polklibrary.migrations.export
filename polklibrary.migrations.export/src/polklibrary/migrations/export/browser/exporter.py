from plone import api
from plone.memoize import ram
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json, logging, time, base64

logger = logging.getLogger("Plone")


def _cache_key(method, self):
    return (self.portal.id, time.time() // (60 * 60))


class Exporter(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
    
        #uids = self.get_cached_uids()
    
        with api.env.adopt_roles(roles=['Manager']):
        
            # Folders one lvl deep
            if self.request.form.get('folder','0') == '1':
                data = self.get_object_data(self.context) # get folder data
            
                all_data = []
                #for brain in self.context.getFolderContents():
                for o in self.context.contentItems():
                    if self.request.form.get('ignore_folderish','0') == '0':
                        all_data.append(self.get_object_data(o[1]))
                    elif not brain.is_folderish:
                        all_data.append(self.get_object_data(o[1]))
                    
                data['__content'] = all_data
                
                return json.dumps(data, indent=4, sort_keys=True)
                
                
            # Single object
            return json.dumps(self.get_object_data(self.context), indent=4, sort_keys=True)
        
    
    def get_object_data(self, obj):
    
        data = {}
        
        # PLONE NATIVE -----------------------------------
        data['portal_type'] = obj.portal_type
        data['_plone.uuid'] = obj.UID()
        data['getId'] = obj.getId()
        data['title'] = obj.title
        
        
        portal_workflow = getToolByName(self.portal, "portal_workflow")
        review_state = portal_workflow.getInfoFor(obj, 'review_state')
        data['review_state'] = review_state
        
        if hasattr(obj, 'description') and obj.description:
            data['description'] = obj.description
            
        if hasattr(obj, 'exclude_from_nav'):
            data['exclude_from_nav'] = obj.exclude_from_nav
        
        if hasattr(obj, 'body') and obj.body and hasattr(obj.body, 'output'):
            content = obj.body.output
            if self.request.form.get('update','0') == '1': 
                content = content.replace('www.uwosh.edu/library', 'library.uwosh.edu')
            data['body:TEXT'] = content
            
        if hasattr(obj, 'text') and obj.text and hasattr(obj.text, 'output'):
            data['text:TEXT'] = obj.text.output
            
        if hasattr(obj, 'getRemoteUrl') and obj.getRemoteUrl:
            data['getRemoteUrl'] = obj.getRemoteUrl
        
        if hasattr(obj, 'start') and obj.start:
            data['start'] = obj.start.strftime("%Y-%m-%d, %H:%M")
        
        if hasattr(obj, 'end') and obj.end:
            data['end'] = obj.end.strftime("%Y-%m-%d, %H:%M")

        if hasattr(obj, 'location') and obj.location:
            data['location'] = obj.location
        
        if hasattr(obj, 'Creator') and obj.Creator():
            data['creator'] = obj.Creator()
            
        if hasattr(obj, 'Subject') and obj.Subject:
            data['subjects'] = obj.Subject()
        
            
        # To Base64 ------------------------------------------
        
        if hasattr(obj, 'image') and obj.image:
            data['image:IMAGE'] = self.to_base64(obj.image.data)
            data['filename'] = obj.image.filename
            
        if hasattr(obj, 'file') and obj.file:
            data['file:FILE'] = self.to_base64(obj.file.data)
            data['filename'] = obj.file.filename
        
        if hasattr(obj, 'json_data') and obj.json_data:
            data['json_data:JSON'] = self.to_base64(obj.json_data)
        
        
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
            data['professional_background:TEXT'] = obj.professional_background.output
            
        if hasattr(obj, 'community_involvment') and obj.community_involvment and hasattr(obj.community_involvment, 'output'):
            data['community_involvment:TEXT'] = obj.community_involvment.output
            
        if hasattr(obj, 'education') and obj.education and hasattr(obj.education, 'output'):
            data['education:TEXT'] = obj.education.output
            
        if hasattr(obj, 'prebody') and obj.prebody and hasattr(obj.prebody, 'output'):
            data['prebody:TEXT'] = obj.prebody.output
            
        if hasattr(obj, 'message') and obj.message and hasattr(obj.message, 'output'):
            data['message:TEXT'] = obj.message.output
            
        if hasattr(obj, 'libchat') and obj.libchat:
            data['libchat'] = obj.libchat
            
        if hasattr(obj, 'suppress_title'):
            data['suppress_title'] = obj.suppress_title
            
        if hasattr(obj, 'suppress_description'):
            data['suppress_description'] = obj.suppress_description
            
        if hasattr(obj, 'set_context') and obj.set_context:
            data['set_context'] = obj.set_context
            
        if hasattr(obj, 'format_type') and obj.format_type:
            data['format_type'] = obj.format_type
            
        if hasattr(obj, 'enabled_browse') and obj.enabled_browse:
            data['enabled_browse'] = obj.enabled_browse
            
        if hasattr(obj, 'limit') and obj.limit:
            data['limit'] = obj.limit
            
        if hasattr(obj, 'query_logic') and obj.query_logic:
            data['query_logic'] = obj.query_logic
            
        if hasattr(obj, 'by_id') and obj.by_id:
            data['by_id'] = obj.by_id
            
        if hasattr(obj, 'subject_heading') and obj.subject_heading:
            data['subject_heading'] = obj.subject_heading
            
        if hasattr(obj, 'series_title') and obj.series_title:
            data['series_title'] = obj.series_title
            
        if hasattr(obj, 'associated_entity') and obj.associated_entity:
            data['associated_entity'] = obj.associated_entity
            
        if hasattr(obj, 'geography') and obj.geography:
            data['geography'] = obj.geography
            
        if hasattr(obj, 'genre') and obj.genre:
            data['genre'] = obj.genre
            
        if hasattr(obj, 'sort_type') and obj.sort_type:
            data['sort_type'] = obj.sort_type
            
        if hasattr(obj, 'sort_direction') and obj.sort_direction:
            data['sort_direction'] = obj.sort_direction
            
        return data
        
    
    def to_base64(self, data):
        return base64.b64encode(data)
    
            
    @ram.cache(_cache_key)
    def get_cached_uids(self):
        print("Creating cached uids")
        results = {}
        #brains = api.content.find()
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog()
        for brain in brains:
            results[brain.UID] = brain.getURL()
        return results
    
    
    @property
    def portal(self):
        return api.portal.get()
        
        
        
class ExporterList(BrowserView):

    output = ""

    def __call__(self):
        #self.request.response.setHeader('Content-Type', 'application/json')
        
        with api.env.adopt_roles(roles=['Manager']):
        
            # Folders one lvl deep
            target = self.request.form.get('target','[NO target PARAMETER PROVIDED]')
    
            for brain in self.context.getFolderContents():
                link =  target + '/polklibrary_import?url=' + brain.getURL() + '/polklibrary_export'
                self.output += '<a target="_blank" href="' + link + '">' + link + '</a> <br />'
            
                
        return self.output
        
    
    @property
    def portal(self):
        return api.portal.get()