import numpy as np
import abc
from typing import List, Tuple, Set
from functools import reduce
from .collidable_physics_configuration import CollidablePhysicsConfiguration
from .polygon import Polygon
from ..vectors import (
    unit,
    normal_vecs,
    magnitude,
    vec_is_nul,
    sign_vec,
    vecs_addition,
    vec2,
    vec_is_in_list,
)
from ..numbers import MAX_FLOAT


class Collidable(abc.ABC):
    def __init__(self):
        super().__init__()
        self.position = vec2()
        self.collision_impulse_stack = vec2()
        self.velocity = vec2()

        # Provide a default physics config
        self.physics_config = CollidablePhysicsConfiguration({})
        # self.submit_to_physical_world()  # init to default global physics settings

        # create a list of points with coordinates relative to position
        self.collider_polygon: Polygon

        # the largest distance between the center and the edges of the polygon.
        self.pre_collision_ray: float

        self.collides_with: Set[Collidable] = set()
        self.collision_events = list()

        # Generate a unique id for when we have no interest in using a real reference of the object
        self.uid = id(self)
        self.name = type(self).__name__

    def set_name(self, name):
        self.name = name

    @abc.abstractmethod
    def init_collider_polygon(self, points: np.array):
        self.collider_polygon = Polygon(points)
        points = self.collider_polygon.points
        cm = self.collider_polygon.center

        max_ray = 0
        for pt in points:
            dist = magnitude(pt - cm)
            if dist > max_ray:
                max_ray = dist

        self.pre_collision_ray = max_ray

    def set_velocity(self, v):
        self.velocity = v

    def push_velocity_correction(self, vec):
        self.set_velocity(self.velocity + vec)

    def apply_inertia(self):
        self.set_velocity(self.velocity / self.physics_config.mass)

    def push_collision_with(self, collidable):
        self.collides_with.add(collidable)

    def push_collision_response(self, vec):
        self.collision_impulse_stack += vec

    def handle_collision_detection_with_group(self, collidable_group, options=dict()):
        collidable_group: List[Collidable] = filter(
            lambda x: not (x is self) and not x.has_null_collider(), collidable_group)

        if not vec_is_nul(self.velocity):
            collidable_group = self.get_directional_raycasted_collidable_group(
                collidable_group, options)
        else:
            collidable_group = self.get_radial_raycasted_collidable_group(
                collidable_group, options)

        for c2 in collidable_group:
            if not self.is_colliding_with(c2):
                self.handle_collision_detection(c2, options)

    def get_polygon_projection(self, axis, use_collider=None):
        collider = use_collider or self.collider_polygon

        proj_points = np.array([(pt + self.position).dot(axis)
                                for pt in collider.points])
        return vec2(np.min(proj_points), np.max(proj_points))

    def get_proj_velocity_extrapolation(self, proj, axis, velocity, extrapolation=None) -> Tuple[float, np.array]:
        extrapolation = extrapolation if extrapolation else abs(
            axis.dot(velocity))

        # Get c1 and c2 velocity projections
        v_proj = axis.dot(velocity)
        abs_v_proj = abs(v_proj)
        offset = 0

        if abs_v_proj > abs(proj[1] - proj[0]):
            proj = vec2(proj[0] - extrapolation,
                        proj[1] + extrapolation)
            offset = extrapolation
        elif v_proj < 0:
            proj = vec2(proj[0] - extrapolation,
                        proj[1])
        else:
            proj = vec2(proj[0],
                        proj[1] + extrapolation)

        return (offset, proj)

    def get_projections_interval_distance(self, proj_1, proj_2) -> float:
        min_a = proj_1[0]
        max_a = proj_1[1]
        min_b = proj_2[0]
        max_b = proj_2[1]
        if min_a < min_b:
            return min_b - max_a
        else:
            return min_a - max_b

    def get_directional_raycasted_collidable_group(self, collidable_group, options=dict()):
        ray_casted_group = list()

        # Get an axis perpendicular to velocity
        v_norm = unit(normal_vecs(self.velocity)[0])

        # Get an axis parallel to velocity
        v_axis = unit(self.velocity)

        v1 = self.velocity
        c1_collider = options.get("use_collider")
        c1_proj = self.get_polygon_projection(v_norm, c1_collider)

        (_offset_proj_c1, c1_proj) = self.get_proj_velocity_extrapolation(
            c1_proj, v_norm, v1)

        c1_v_proj = self.get_polygon_projection(v_axis, c1_collider)

        (offset_v_proj_c1, c1_v_proj) = self.get_proj_velocity_extrapolation(
            c1_v_proj, v_axis, v1)

        for c2 in collidable_group:
            c2_proj = c2.get_polygon_projection(v_norm)
            (_offset_proj_c2, c2_proj) = self.get_proj_velocity_extrapolation(
                c2_proj, v_norm, c2.velocity)

            d = self.get_projections_interval_distance(c1_proj, c2_proj)

            if d < 0:
                v2 = c2.velocity
                c2_v1_proj = c2.get_polygon_projection(v_axis)
                (offset_v_proj_c2, c2_v1_proj) = self.get_proj_velocity_extrapolation(
                    c2_v1_proj, v_axis, v2, v2.dot(v_axis))

                distance = (c2_v1_proj[0]
                            - c1_v_proj[1]
                            + offset_v_proj_c1
                            + offset_v_proj_c2)

                min_distance = c2_v1_proj[1] - c1_v_proj[0]
                if min_distance > 0 and distance < self.pre_collision_ray + c2.pre_collision_ray:
                    result = {"collidable": c2, "distance": distance}
                    ray_casted_group.append(result)

        ray_casted_group.sort(key=lambda r: r["distance"])
        return {r["collidable"] for r in ray_casted_group}

    def get_radial_raycasted_collidable_group(self, collidable_group, options=dict()):
        """
        Returns the portion of the paramter collidable group wich is in the potential collision area of the instance
        """
        c1_center_pos = self.get_center_position(options.get("use_collider"))

        def is_in_collision_area(collidable):
            c2 = collidable
            distance = c1_center_pos - c2.get_center_position()
            axis = unit(distance)
            v2 = c2.velocity
            ray_2 = c2.pre_collision_ray
            ray_1 = self.pre_collision_ray
            min_dist = ray_2 + axis.dot(v2) + ray_1
            tolerance_offset = 0
            return magnitude(distance) < min_dist + tolerance_offset

        return {c for c in collidable_group if is_in_collision_area(c)}

    def has_null_collider(self):
        return not np.any(self.collider_polygon)

    def handle_collision_detection(self, collidable, options=dict()):
        """
        Separating axis algorithm
        """
        c2: Collidable = collidable
        min_distance = MAX_FLOAT
        separating_vec = vec2()
        intersect = True
        will_intersect = True
        v1 = self.velocity
        v2 = c2.velocity
        polys_center_vec = self.get_center_position() - c2.get_center_position()

        c1_collider = options.get("use_collider", self.collider_polygon)
        c2_collider = options.get("c2_collider", c2.collider_polygon)

        for seg in np.concatenate((c1_collider.segments, c2_collider.segments)):
            # Create the projection axis for that segment
            axis = unit(
                normal_vecs(
                    seg[1] - seg[0]
                )[0]
            )

            # Get collidable c1 projection on axis
            proj_c1 = self.get_polygon_projection(axis, c1_collider)
            proj_c2 = c2.get_polygon_projection(axis, c2_collider)

            # Check distance between projections of the 2 polygons
            distance = self.get_projections_interval_distance(proj_c1, proj_c2)

            if distance > 0:
                intersect = False

            # Update projections with velocity extrapolation.
            v_dif_proj = axis.dot(v1 - v2)
            abs_v_dif_proj = abs(v_dif_proj)

            (offset_proj_c1, proj_c1) = self.get_proj_velocity_extrapolation(
                proj_c1, axis, v1, abs_v_dif_proj)

            (offset_proj_c2, proj_c2) = self.get_proj_velocity_extrapolation(
                proj_c2, axis, v2, abs_v_dif_proj)

            # Check distance again to detect a future collision with velocity extrapolated
            add_offset = 0
            if not vec_is_nul(v1) and offset_proj_c2 != 0:
                add_offset += offset_proj_c2
            if not vec_is_nul(v2) and offset_proj_c1 != 0:
                add_offset += offset_proj_c1

            distance = self.get_projections_interval_distance(
                proj_c1, proj_c2) + add_offset

            if distance > 0:
                will_intersect = False

            if not intersect and not will_intersect:
                break

            # If the distance is the smallest we found so far, we update the response vector
            distance = abs(distance)
            if distance < min_distance:
                min_distance = distance
                separating_vec = axis

        if will_intersect:
            response_mode = options.get("response_mode", "solid")
            notify_both = options.get("notify_collision_both", False)

            if response_mode == "solid" and c2.physics_config.solid:
                c2_movable = c2.physics_config.movable

                response = separating_vec * min_distance
                n = separating_vec

                c1_transfer_prio = self.physics_config.velocity_transfer_priority
                c2_transfer_prio = c2.physics_config.velocity_transfer_priority
                if c1_transfer_prio == c2_transfer_prio:
                    prior_c1 = v1.dot(n) < v2.dot(-n)
                    if prior_c1:
                        c1_transfer_prio += 1
                    else:
                        c2_transfer_prio += 1

                centers_vec_scale = polys_center_vec.dot(n)

                response = -response if centers_vec_scale < 0 else response

                # Collision response negociation.
                # For a plastic collision only one of the two collidables should apply the minimum translation vector
                should_transfer_c1 = not c2_movable or c1_transfer_prio > c2_transfer_prio
                response_c1 = response * int(should_transfer_c1)

                if notify_both:
                    should_transfer_c2 = c2_movable and c2_transfer_prio > c1_transfer_prio
                    response_c2 = -response * int(should_transfer_c2)

                    c2.push_collision_response(response_c2)

                self.push_collision_response(response_c1)

            self.push_collision_with(c2)
            if options.get("notify_collision_both"):
                c2.push_collision_with(self)

    def apply_collisions(self):
        if not vec_is_nul(self.collision_impulse_stack):
            self.set_velocity(self.velocity + self.collision_impulse_stack)

    def is_colliding_with(self, collidable):
        return collidable in self.collides_with

    def flush_collisions(self):
        if len(self.collides_with) > 0:
            self.collides_with = set()
            self.collision_impulse_stack = vec2()

    def flush(self):
        self.flush_collisions()

    def set_physics_config(self, physics_config: CollidablePhysicsConfiguration):
        """
        Sets the physics_config field of the instance with a CollidablePhysicsConfiguration object
        """
        self.physics_config = physics_config

    def set_position(self, x: float, y: float):
        """
        Update the instance's position with x y parameters
        """
        self.position = vec2(x, y)

    def get_center_position(self, use_collider=None):
        """
        Returns the instance's center position
        """
        collider = use_collider or self.collider_polygon
        return collider.center + self.position

    def update_position(self):
        """
        Applys the instance's velocity vector state on its position.
        """
        self.position = self.position + self.velocity

    def get_name(self):
        return getattr(self, "name", type(self).__name__)
