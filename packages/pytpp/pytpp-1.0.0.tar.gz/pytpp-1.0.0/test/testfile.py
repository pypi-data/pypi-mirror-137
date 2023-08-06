from pytpp import Authenticate, Scope

scope = Scope()
scope.certificate(approve=True)
scope.security(delete=True)

api = Authenticate('mctpp1.venspi.eng.venafi.com', 'admin', 'newPassw0rd!')

print('done')
