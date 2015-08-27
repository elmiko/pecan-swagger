# pecan-swagger-REST
swagger generator for pecan RestController APIs

## How to use

1. Place pecan-swagger into your project directory.
2. Fill in the blanks at the top of `swag/swag.py` with the path to your RootController

        from ____ import ____ as root_controller
    for example

        from my_project.api.controllers import root.RootController as root_controller

3. Decorate any _lookup functions in your project with @methodroute. The first argument
is the parameter passed to _lookup, and the 2nd argument is the Controller to route to. Like so
        
        @methodroute('car_model', 'CarController')
        _lookup(self, primary_key, *remainder):
            car = getcar(primary_key)
                return CarController(car), remainder

4. In case `CarController` is called from an imported module as in `vehicles.CarController`,
don't forget to import it for pecan-swagger to locate. Like so

        from vehicles import CarController

5. Open terminal and run `python swag.py` and collect swagger from output or pipe it wherever you want!
