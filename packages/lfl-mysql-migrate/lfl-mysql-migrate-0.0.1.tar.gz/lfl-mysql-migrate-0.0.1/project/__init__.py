def get_LOGGING( log_file_name , log_file_name1 ) :
    return {
        'version' : 1 ,
        'disable_existing_loggers' : False ,
        'formatters' : {
            'verbose' : {
                'format' : '{levelname} {asctime} {module} {process:d} {thread:d} {message}' ,
                'style' : '{' ,
            } ,
            'simple' : {
                'format' : '{levelname} {module}  {message}' ,
                'style' : '{' ,
            } ,
        } ,
        'handlers' : {
            # 'file' : {
            #     'level' : 'DEBUG' ,
            #     'class' : 'logging.FileHandler' ,
            #     'filename' : log_file_name ,
            #     'formatter' : 'simple'
            # } ,
            'file1' : {
                'level' : 'DEBUG' ,
                'class' : 'logging.FileHandler' ,
                'filename' : log_file_name1 ,
                'formatter' : 'verbose'
            } ,
            'file' : {
                'level' : 'DEBUG' ,
                'class' : 'logging.FileHandler' ,
                'filename' : log_file_name ,
                'formatter' : 'verbose'
            } ,
        } ,
        'loggers' : {
            'sitelfl.management.commands.migrate-base' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-one' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-calendar' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-persons' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-clubs' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-construction' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-players' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.migrate-referees' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.fill_images' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'lfl_admin.common.models.model_images' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.check_old_files' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'lfl_admin.common.management.commands.check_unbounded_image_files' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.check_and_copy_dumps' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.check_git_commit' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'isc_common.models.model_images' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands.sync_lfl_base' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'sitelfl.management.commands' : {
                'handlers' : [ 'file' ] ,
                'level' : 'DEBUG' ,
            } ,
            'django' : {
                'handlers' : [ 'file' ] ,
                'level' : 'INFO' ,
            } ,
        } ,
    }


def get_INSTALLED_APPS() :
    return [
        'isc_common' ,
        'sitelfl' ,
        'lfl_admin.common' ,
        'lfl_admin.competitions' ,
        'lfl_admin.constructions' ,
        'lfl_admin.decor' ,
        'lfl_admin.inventory' ,
        'lfl_admin.region' ,
        'lfl_admin.user_ext' ,
        'django.contrib.admin' ,
        'django.contrib.auth' ,
        'django.contrib.contenttypes' ,
        'django.contrib.sessions' ,
        'django.contrib.messages' ,
        'django.contrib.staticfiles' ,
    ]


def get_STATICFILES_DIRS( BASE_DIR ) :
    return [
        ("common" , f"{BASE_DIR}/static") ,
        ("isc" , f"{BASE_DIR}/node_modules/npm-smartclient/dest") ,
        ("isc-ts" , f"{BASE_DIR}/dest") ,
        ("isomorphic" , f"{BASE_DIR}/node_modules/npm-smartclient/isomorphic") ,
        ("dropzone" , f"{BASE_DIR}/node_modules/npm-smartclient/dropzone") ,
    ]


def get_TEMPLATES() :
    return [
        {
            'BACKEND' : 'django.template.backends.django.DjangoTemplates' ,
            'DIRS' : [ ] ,
            'APP_DIRS' : True ,
            'OPTIONS' : {
                'context_processors' : [
                    'django.template.context_processors.debug' ,
                    'django.template.context_processors.request' ,
                    'django.contrib.auth.context_processors.auth' ,
                    'django.contrib.messages.context_processors.messages' ,
                ] ,
            } ,
        } ,
    ]


def get_MIDDLEWARE() :
    return [
        'django.middleware.security.SecurityMiddleware' ,
        'django.contrib.sessions.middleware.SessionMiddleware' ,
        'django.middleware.common.CommonMiddleware' ,
        'django.middleware.csrf.CsrfViewMiddleware' ,
        'django.contrib.auth.middleware.AuthenticationMiddleware' ,
        'django.contrib.messages.middleware.MessageMiddleware' ,
        'django.middleware.clickjacking.XFrameOptionsMiddleware' ,
    ]


def get_AUTH_PASSWORD_VALIDATORS() :
    return [
        {
            'NAME' : 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' ,
        } ,
        {
            'NAME' : 'django.contrib.auth.password_validation.MinimumLengthValidator' ,
        } ,
        {
            'NAME' : 'django.contrib.auth.password_validation.CommonPasswordValidator' ,
        } ,
        {
            'NAME' : 'django.contrib.auth.password_validation.NumericPasswordValidator' ,
        } ,
    ]
