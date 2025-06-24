# Python
from flask import (
    Flask, render_template, redirect, url_for,
    flash
)
from flask_migrate import Migrate

from forms import (
    OwnerForm, DogForm, WalkerForm,
    AvailabilityForm
)
from models import db, DogOwner, Dog, DogWalker, Availability


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="REPLACE_WITH_YOUR_SECRET",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{app.instance_path}/dogmatch.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    Migrate(app, db)
    return app


app = create_app()


# ------------------------------------------------------------------ Routes ---

@app.route("/")
def home():
    return render_template("index.html")


# Owner CRUD
@app.route("/owners")
def owners():
    owners = DogOwner.query.all()
    return render_template("owners.html", owners=owners)


@app.route("/owners/add", methods=["GET", "POST"])
def add_owner():
    form = OwnerForm()
    if form.validate_on_submit():
        owner = DogOwner(name=form.name.data, email=form.email.data)
        db.session.add(owner)
        db.session.commit()
        flash("Owner added", "success")
        return redirect(url_for("owners"))
    return render_template("owner_form.html", form=form)


@app.route("/owners/<int:owner_id>/edit", methods=["GET", "POST"])
def edit_owner(owner_id):
    owner = DogOwner.query.get_or_404(owner_id)
    form = OwnerForm(obj=owner)
    if form.validate_on_submit():
        form.populate_obj(owner)
        db.session.commit()
        flash("Owner updated", "success")
        return redirect(url_for("owners"))
    return render_template("owner_form.html", form=form)


# Dog CRUD
@app.route("/dogs")
def dogs():
    dogs = Dog.query.all()
    return render_template("dogs.html", dogs=dogs)


@app.route("/dogs/add", methods=["GET", "POST"])
def add_dog():
    form = DogForm()
    if form.validate_on_submit():
        dog = Dog(
            name=form.name.data,
            breed=form.breed.data,
            owner_id=form.owner_id.data
        )
        db.session.add(dog)
        db.session.commit()
        flash("Dog added", "success")
        return redirect(url_for("dogs"))
    return render_template("dog_form.html", form=form)


@app.route("/dogs/<int:dog_id>/edit", methods=["GET", "POST"])
def edit_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    form = DogForm(obj=dog)
    if form.validate_on_submit():
        form.populate_obj(dog)
        db.session.commit()
        flash("Dog updated", "success")
        return redirect(url_for("dogs"))
    return render_template("dog_form.html", form=form)


# Walker CRUD
@app.route("/walkers")
def walkers():
    walkers = DogWalker.query.all()
    return render_template("walkers.html", walkers=walkers)


@app.route("/walkers/add", methods=["GET", "POST"])
def add_walker():
    form = WalkerForm()
    if form.validate_on_submit():
        walker = DogWalker(
            name=form.name.data,
            phone=form.phone.data
        )
        db.session.add(walker)
        db.session.commit()
        flash("Walker added", "success")
        return redirect(url_for("walkers"))
    return render_template("walker_form.html", form=form)


@app.route("/walkers/<int:walker_id>/edit", methods=["GET", "POST"])
def edit_walker(walker_id):
    walker = DogWalker.query.get_or_404(walker_id)
    form = WalkerForm(obj=walker)
    if form.validate_on_submit():
        form.populate_obj(walker)
        db.session.commit()
        flash("Walker updated", "success")
        return redirect(url_for("walkers"))
    return render_template("walker_form.html", form=form)


# Availability CRUD (shared by Dog & Walker)
@app.route("/availability/<string:entity>/<int:entity_id>", methods=["GET", "POST"])
def manage_availability(entity, entity_id):
    form = AvailabilityForm()
    if entity == "dog":
        obj = Dog.query.get_or_404(entity_id)
        redirect_endpoint = "dogs"
    else:
        obj = DogWalker.query.get_or_404(entity_id)
        redirect_endpoint = "walkers"

    if form.validate_on_submit():
        avail = Availability(
            weekday=form.weekday.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            dog=obj if entity == "dog" else None,
            walker=obj if entity == "walker" else None,
        )
        db.session.add(avail)
        db.session.commit()
        flash("Availability added", "success")
        return redirect(url_for(redirect_endpoint))

    return render_template(
        "availability_form.html",
        form=form,
        entity=entity,
        obj=obj
    )


# Matching --------------------------------------------------------------------

def overlaps(a_start, a_end, b_start, b_end):
    return max(a_start, b_start) < min(a_end, b_end)


@app.route("/match")
def match():
    matches = []  # list of (dog, walker, weekday, start, end)
    dogs = Dog.query.all()
    walkers = DogWalker.query.all()

    for dog in dogs:
        for walker in walkers:
            for da in dog.availabilities:
                for wa in walker.availabilities:
                    if da.weekday == wa.weekday and overlaps(
                            da.start_time, da.end_time, wa.start_time, wa.end_time
                    ):
                        start = max(da.start_time, wa.start_time)
                        end = min(da.end_time, wa.end_time)
                        matches.append((dog, walker, da.weekday, start, end))
    return render_template("match.html", matches=matches)
