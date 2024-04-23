# Author: https://github.com/mauroreisvieira/github-sublime-theme/
from fractions import gcd

class Fractions:
    """Some comment
    In a galaxy far, far away~"""
    def __init__(self, nom, denom):
        self.nom = nom
        self.denom = denom
        self.__reduce()

    def __reduce(self):
        GCD = gcd(self.nom, self.denom)
        self.nom, self.denom = self.nom // GCD, self.denom // GCD

    def __str__(self):
        if self.nom/self.denom >= 1:
            integer = self.nom // self.denom
            flt = Fractions(self.nom % self.denom, self.denom)
            if flt.nom == 0:
                return str(integer)
            else:
                return str(integer)+' '+str(flt)
        else:
            return str(self.nom)+'/'+str(self.denom)

    def __add__(self, other):
        nom = self.nom*other.denom + self.denom*other.nom
        denom = self.denom * other.denom
        return Fractions(nom, denom)

    def __sub__(self, other):
        nom = self.nom*other.denom - self.denom*other.nom
        denom = self.denom * other.denom
        return Fractions(nom, denom)

    def __truediv__(self, other):
        nom, denom = self.nom*other.denom, self.denom*other.nom
        return Fractions(nom, denom)

    def __mul__(self, other):
        nom, denom = self.nom * other.nom, self.denom * other.denom
        return Fractions(nom, denom)

    def __copy__(self):
        return Fractions(self.nom, self.denom)

    def __pow__(self, power, modulo=None):
        ret = self.__copy__()

        if power == 0:
            return Fractions(1,1)
        elif power < 0:
            for _ in range(abs(power)-1):
                ret *= self
            return Fractions(1,1)/ret
        else:
            for _ in range(abs(power)):
                ret *= self
            return ret

    def __eq__(self, other):
        return self.nom == other.nom and self.denom == other.denom

    def astuple(self):
        return self.nom, self.denom

    def destroy(self):
        self.nom = None
        self.denom = None

my_frac1 = Fractions(20, 30)
my_frac2 = Fractions(5, 173)

my_frac1.destroy()

print(my_frac1)
print(my_frac1 == my_frac1.__copy__())
print(my_frac1 / (my_frac1 - my_frac2))

from functools import reduce
from .models import Base, User, Org, Repo, Issue, OrgRole, RepoRole, role

class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    base_repo_role = Column(String)
    billing_address = Column(String)

    def repr(self):
        return {
            "id": self.id,
            "name": self.name,
            "billing_address": self.billing_address,
            "base_repo_role": self.base_repo_role,
        }

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

    def repr(self):
        return {"id": self.id, "email": self.email}

   @app.before_request
    def set_current_user_and_session():
        flask_session.permanent = True

        g.session = Session()
        # docs: begin-authn
        if "current_user" not in g:
            if "current_user_id" in flask_session:
                user_id = flask_session.get("current_user_id")
                user = g.session.query(User).filter_by(id=user_id).one_or_none()
                if user is None:
                    flask_session.pop("current_user_id")
                g.current_user = user
            else:
                g.current_user = None
        # docs: end-authn

    @app.after_request
    def add_cors_headers(res):
        res.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        res.headers.add("Access-Control-Allow-Headers", "Accept,Content-Type")
        res.headers.add("Access-Control-Allow-Methods", "DELETE,GET,OPTIONS,PATCH,POST")
        res.headers.add("Access-Control-Allow-Credentials", "true")
        return res

    @app.after_request
    def close_session(res):
        if "session" in g:
            g.session.close()
        return res

    return app

from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
    

def stringify(x: int) -> str:
    return str(x)

def shadow_update_dict(d1: dict, d2: dict) -> Mapping:
    return ChainMap(d2, d1)

    """Add two numbers and return the result."""

    """
    >>> my_function(2, 3)
    6
    >>> my_function('a', 3)
    'aaa'
    """
