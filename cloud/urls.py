
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='index'),
    path('home',views.index,name='home'),
    path('files',views.login,name='files'),
    #path('upload',views.login,name='upload'),
    path('file',views.upload,name='file'),
    path('storage',views.web,name='storage'),
    path('ipfsdata',views.validate,name='ipfsdata'),
    path('retrieve',views.retrive,name='retrieve'),
    path('addfile',views.ipfs_add,name='addfile'),
    # #path('home',views.getmeta,name='home'),
    path('valid',views.validation,name='valid'),
    path('test',views.test,name='test'),
    path('upload_files',views.upload_page,name='upload_files'),
    path('upload_Files',views.upload_Files,name='upload_Files'),
    path('deletetask',views.deletetask),
    path('old_deletetask/<int:taskpk>/',views.deletetask),
    path('download',views.download,name='download'),
    # testing url
    path('test1',views.test1,name='test1'),
    path('testdelete',views.testdelete,name='testdelete'),
    path('test2',views.test2,name='test2'),
]