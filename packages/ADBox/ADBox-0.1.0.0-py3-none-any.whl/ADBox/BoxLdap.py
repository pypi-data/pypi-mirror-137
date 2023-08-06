import ldap3


class BoxLdap(object):
    # Server - Active Directory server {ip/domain name}
    # User - login user name {domain\samaccountname}
    # Password - user password
    # UseSSL - port 389/636
    # MainLogger - logger object
    def __init__(self, Server, User, Password, UseSSL, MainLogger, ):
        self.__LdapLogger = MainLogger
        self._ConnectStatus = False
        self.__LdapLogger.debug("BoxLdap.__init__: init class")
        if(UseSSL==True):
            LdapPort = 636
        else:
            LdapPort = 389
        self.__ADServer = ldap3.Server(Server, port=LdapPort, use_ssl=UseSSL)
        self.__LdapLogger.debug("BoxLdap.__init__: Config server - ldap://{0}:{1}".format(Server,LdapPort))
        try:
            self.__ADConnect = ldap3.Connection(self.__ADServer, User, Password,
                                                client_strategy=ldap3.SAFE_SYNC, auto_bind=True)
        except Exception as LdapExcept:
            self.__LdapLogger.error("BoxLdap.__init__: {0}".format(LdapExcept))
        else:
            self._ConnectStatus = True
            self.__LdapLogger.info("BoxLdap.__init__: Bind successful")
            self._ADRoot = self.__ADServer.schema.schema_entry[self.__ADServer.schema.schema_entry.find("DC="):]
            self.__LdapLogger.info("BoxLdap.__init__: AD root - {0}".format(self._ADRoot))

    def GetUsers(self,MainBoxSql):
        SearchResult = self.__ADConnect.search(search_base=self._ADRoot, search_filter="(&(objectClass=user)(objectCategory=person))", search_scope=ldap3.SUBTREE, attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES])
        # (&(objectClass=user)(objectCategory=person))
        # (sAMAccountType=805306368)
        for Entry in SearchResult[2]:
            if(Entry["type"]=="searchResEntry"):
                try:
                    MainBoxSql.AddUser(Entry["attributes"]["distinguishedName"], Entry["attributes"]["sAMAccountName"], Entry["attributes"]["userAccountControl"], Entry["attributes"])
                except Exception as LdapExcept:
                    self.__LdapLogger.error("BoxLdap.GetUsers: Fail add user - {0}".format(LdapExcept))
        self.__LdapLogger.info("BoxLdap.GetUsers: Add {0} users".format(len(SearchResult[2])))

    def GetComputers(self,MainBoxSql):
        SearchResult = self.__ADConnect.search(search_base=self._ADRoot, search_filter="(objectCategory=computer)", search_scope=ldap3.SUBTREE, attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES])
        for Entry in SearchResult[2]:
            if(Entry["type"]=="searchResEntry"):
                try:
                    MainBoxSql.AddComputer(Entry["attributes"]["distinguishedName"], Entry["attributes"]["sAMAccountName"], Entry["attributes"]["userAccountControl"], Entry["attributes"])
                except Exception as LdapExcept:
                    self.__LdapLogger.error("BoxLdap.GetComputers: Fail add computer - {0}".format(LdapExcept))
        self.__LdapLogger.info("BoxLdap.GetComputers: Add {0} computers".format(len(SearchResult[2])))


    def GetGroups(self,MainBoxSql):
        SearchResult = self.__ADConnect.search(search_base=self._ADRoot, search_filter="(objectclass=group)", search_scope=ldap3.SUBTREE, attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES])
        for Entry in SearchResult[2]:
            if(Entry["type"]=="searchResEntry"):
                try:
                    MainBoxSql.AddGroup(Entry["attributes"]["distinguishedName"], Entry["attributes"]["sAMAccountName"], Entry["attributes"])
                except Exception as LdapExcept:
                    self.__LdapLogger.error("BoxLdap.GetGroups: Fail add group - {0}".format(LdapExcept))
        self.__LdapLogger.info("BoxLdap.GetGroups: Found {0} groups".format(len(SearchResult[2])))