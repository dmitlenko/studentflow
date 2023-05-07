from rolepermissions.roles import AbstractUserRole

class Permissions:
    PostCreate = 'post_create'
    PostUpdate = 'post_update'
    PostDelete = 'post_delete'
    PostStats = 'post_stats'
    PostCommentCreate = 'post_comment_create'
    PostCommentDelete = 'post_comment_delete'
    UserFileList = 'user_file_list'
    UserFileListUpload = 'user_file_list_upload'
    UserFileListDelete = 'user_file_list_delete'
    AdminPost = 'admin_post'
    AdminPostPublish = 'admin_post_publish'

class Student(AbstractUserRole):
    id = 1
    available_permissons = {
        Permissions.PostCreate: True,
        Permissions.PostUpdate: True,
        Permissions.PostDelete: True,
        Permissions.PostStats: True,
        Permissions.PostCommentCreate: True,
        Permissions.PostCommentDelete: True,
        Permissions.UserFileList: True,
        Permissions.UserFileListUpload: True,
        Permissions.UserFileListDelete: True,
    }

class Teacher(AbstractUserRole):
    id = 2
    available_permissons = Student.available_permissons | {
        Permissions.AdminPost: True,
        Permissions.AdminPostPublish: True
    }