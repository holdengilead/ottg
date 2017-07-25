from fabric.api import env, execute, run

env.use_ssh_config = True
env.roledefs = {
    "staging": ['staging_superlists']
}


def _get_manage_dot_py(host):
    aux = '~/sites/{0}/virtualenv/bin/python ~/sites/{0}/source/manage.py'
    return aux.format(host)


def _flush_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    run('{} flush --noinput'.format(manage_dot_py))


def reset_database(host):
    execute(_flush_database, host, roles=['staging'])


def _create_session(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    return run('{} create_session {}'.format(manage_dot_py, email))


def create_session_on_server(host, email):
    session_key = execute(_create_session, host, email, roles=['staging'])
    return session_key['staging_superlists'].strip()
