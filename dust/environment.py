from particle import Particle
from vector import Vector


class Environment:

    def __init__(self, particles: list, **kwargs):
        """Initialise environment with a list of particles."""
        self.particles = particles
        self.g = kwargs.get('gravity', 0.1)

    def collisions(self):
        """Function checks for collisions between particles and merges
        colliding particles."""
        for i, current in enumerate(self.particles):
            for j, other in enumerate(self.particles):
                if i == j:
                    pass
                else:
                    if current % other:
                        # add other particle to current
                        self.particles[i] = current + other
                        # delete other particle from list
                        del self.particles[j]
                    else:
                        pass

    def move(self):
        """Update system of particles to new position after timestep."""
        forces = Particle.quick_force(self.particles)
        for p, f in zip(self.particles, forces):
            p.update(f)

    def step(self):
        self.move()
        self.collisions()

    @classmethod
    def random_static(cls, n=5, rho=0.2):
        """Create system of n static particles with random positions within the
        window size"""
        particles = []
        for i in range(n):
            particles.append(Particle.random_static(rho))
        return cls(particles)

    @classmethod
    def rotating(cls, n, l=0, **kwargs) -> 'Environment':
        rho = kwargs.pop('density', 0.2)
        particles = [Particle.random_static(rho=rho) for _ in range(n)]
        com = sum(particles).position
        for particle in particles:
            r = particle.position - com
            u = r.unit_vector().rotate(90)
            particle.momentum = l * u
        return cls(particles, **kwargs)
