import math
import openmc
import openmc.deplete as dpl

# define materialsl
fuel = openmc.Material(name="uo2")
fuel.add_element("U", 1, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2)
fuel.set_density("g/cc", 10.4)

clad = openmc.Material(name="clad")
clad.add_element("Zr", 1)
clad.set_density("g/cc", 6)

water = openmc.Material(name="water")
water.add_element("O", 1)
water.add_element("H", 2)
water.set_density("g/cc", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")
materials = openmc.Materials([fuel, clad, water])

fuel.set_density("g/cc", 10.4)

# build geometry
radii = [0.42, 0.45]
pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_univ = openmc.model.pin(pin_surfaces, materials)
b = 1.24 # dimension of bounding box
bound_box = openmc.rectangular_prism(b, b, boundary_type="reflective")
root_cell = openmc.Cell(fill=pin_univ, region=bound_box)
geometry = openmc.Geometry([root_cell])

# doing 2D so assign "volume"
fuel.volume = math.pi * radii[0] ** 2

# set up depletion
chain = dpl.Chain.from_xml('casl_pwr_chain.xml')

# process results