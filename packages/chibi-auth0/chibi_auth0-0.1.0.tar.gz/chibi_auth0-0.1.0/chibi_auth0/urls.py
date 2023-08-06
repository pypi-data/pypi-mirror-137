from chibi_requests import Chibi_url


well_know = Chibi_url( "https://{domain}/.well-known/jwks.json" )

auth_token = Chibi_url( 'https://{domain}/oauth/token' )

user = Chibi_url( 'https://{domain}/api/v2/users/{user_id}' )

user_info = Chibi_url( 'https://{domain}/userinfo' )
