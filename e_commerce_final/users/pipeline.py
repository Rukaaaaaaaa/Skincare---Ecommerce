from social_core.exceptions import AuthAlreadyAssociated

def prevent_duplicate_google_linkage(backend, uid, user=None, social=None, *args, **kwargs):
    existing_social = backend.strategy.storage.user.get_social_auth(backend.name, uid)

    if existing_social:
        # Nếu tài khoản Google đã được liên kết với người khác
        if user and existing_social.user != user:
            raise AuthAlreadyAssociated(backend, 'Tài khoản Google này đã được liên kết với một người dùng khác.')
