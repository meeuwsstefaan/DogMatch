from datetime import timedelta, datetime

from flask import (
    Flask, render_template, redirect, url_for,
    flash, request
)
from flask_migrate import Migrate

from forms import (
    OwnerForm, DogForm, WalkerForm,
    AvailabilityForm
)
from models import db, DogOwner, Dog, DogWalker, Availability, Matches

MINIMUM_OVERLAP_MINUTES = 15


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

if __name__ == "__main__":
    app.debug = False
    app.run(host="192.168.129.2", port=5000, debug=False)


# ------------------------------------------------------------------ Routes ---


@app.route("/")
def home():
    return render_template("index.html")


# Owner CRUD
@app.route("/owners")
def owners():
    owners = DogOwner.query.order_by(DogOwner.name.asc()).all()
    table_name = DogOwner.__tablename__
    return render_template("owners.html", owners=owners)


@app.route("/owners/add", methods=["GET", "POST"])
def add_owner():
    form = OwnerForm()
    if form.validate_on_submit():
        owner = DogOwner(name=form.name.data, email=form.email.data, phone=form.phone.data)
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


@app.route("/owners/<int:owner_id>/delete", methods=["POST"])
def delete_owner(owner_id):
    owner = DogOwner.query.get_or_404(owner_id)
    db.session.delete(owner)
    db.session.commit()
    flash("Owner deleted successfully", "success")
    return redirect(url_for("owners"))


# Dog CRUD
@app.route("/dogs")
def dogs():
    dogs = Dog.query.order_by(Dog.name.asc()).all()
    table_name = Dog.__tablename__
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


@app.route("/walkers/<int:walker_id>/delete", methods=["POST"])
def delete_walker(walker_id):
    walker = DogWalker.query.get_or_404(walker_id)
    db.session.delete(walker)
    db.session.commit()
    flash("Dog walker deleted successfully", "success")
    return redirect(url_for("walkers"))


@app.route("/dogs/<int:dog_id>/delete", methods=["POST"])
def delete_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    db.session.delete(dog)
    db.session.commit()
    flash("Dog deleted successfully", "success")
    return redirect(url_for("dogs"))


# Walker CRUD
@app.route("/walkers")
def walkers():
    walkers = DogWalker.query.order_by(DogWalker.name.asc()).all()
    table_name = DogWalker.__tablename__
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
    else:
        obj = DogWalker.query.get_or_404(entity_id)

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

        # Sort the availabilities by weekday
        obj.availabilities.sort(key=lambda a: a.weekday)

        # Instead of redirecting, return the form again with the success message
        return render_template(
            "availability_form.html",
            form=form,
            entity=entity,
            obj=obj,
            success="Availability added"
        )

    return render_template(
        "availability_form.html",
        form=AvailabilityForm(),
        entity=entity,
        obj=obj
    )


@app.route("/availability/<int:availability_id>/delete", methods=["POST"])
def delete_availability(availability_id):
    # Look up the availability entry
    availability = Availability.query.get_or_404(availability_id)

    # Delete the entry
    db.session.delete(availability)
    db.session.commit()

    # Flash the success message and redirect back to the referring page
    flash("Availability deleted successfully", "success")
    return redirect(request.referrer or url_for("home"))


# Matching --------------------------------------------------------------------

def overlaps(a_start, a_end, b_start, b_end):
    # Convert datetime.time objects to datetime.datetime objects for arithmetic
    today = datetime.today()
    a_start_dt = datetime.combine(today, a_start)
    a_end_dt = datetime.combine(today, a_end)
    b_start_dt = datetime.combine(today, b_start)
    b_end_dt = datetime.combine(today, b_end)

    # Determine overlap start and end times
    overlap_start = max(a_start_dt, b_start_dt)
    overlap_end = min(a_end_dt, b_end_dt)

    # Calculate the overlap duration
    overlap_duration = (overlap_end - overlap_start)

    # Check of the overlap duration is at least the defined threshold
    return overlap_duration >= timedelta(minutes=MINIMUM_OVERLAP_MINUTES)
    # return max(a_start, b_start) < min(a_end, b_end)


@app.route("/match")
def match():
    # Clear the Matches table before repopulating it
    Matches.query.delete()
    db.session.commit()

    matches = []  # list of dictionaries
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

                        # Add to the Matches table in the database
                        match = Matches(
                            field1=dog.name,  # Replace with actual fields
                            field2=walker.name  # Replace with actual fields
                        )
                        db.session.add(match)
                        db.session.flush()  # Need to flush to get the match ID

                        matches.append({
                            "id": match.id,  # Use the ID from the database
                            "dog": dog,
                            "walker": walker,
                            "weekday": da.weekday,
                            "start_time": start,
                            "end_time": end,
                        })

    db.session.commit()  # Commit all matches to DB
    matches.sort(key=lambda x: x["dog"].name.lower())
    return render_template("match.html", matches=matches)
