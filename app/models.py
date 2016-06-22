from . import db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    plandb_id = db.Column(db.Integer, db.ForeignKey('plans.id'), default=1)


    def __repr__(self):
        return '<User %r>' % self.username


class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), unique=True)
    amount = db.Column(db.Integer)
    users = db.relationship('User', backref='plan', lazy='dynamic')

    @staticmethod
    def insert_plan_descriptions():
        plan_descriptions = {
            'Individual (Yearly)': (1, 'individual_yearly', 20000),
            'Individual (Monthly)': (2, 'individual_monthly', 2000),
            'Team (Yearly)': (3, 'team_yearly', 100000),
            'Team (Monthly)': (4, 'team_monthly', 10000)
        }
        for p in plan_descriptions:
            plan = Plan.query.filter_by(name = p).first()
            if plan is None:
                plan=Plan(id=plan_descriptions[p][0], name=p,
                          plan_id=plan_descriptions[p][1],
                          amount=plan_descriptions[p][2])
            db.session.add(plan)
        db.session.commit()

    def __repr__(self):
        return '<Plan %r %r >' % (self.name, self.users)
