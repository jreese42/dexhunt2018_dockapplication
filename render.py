class Renderable:
    def __init__(this, obj, x, y, alpha=100):
        this.obj = obj
        this.x = x
        this.y = y
        this.alpha = alpha
    def get_object(this):
        return this.obj
    def get_x(this):
        return this.x
    def get_y(this):
        return this.y
    def get_alpha(this):
        return this.alpha

class Renderer:
    def __init__(this, screen):
        this.shaders = []
        this.objects = []
        this.screen = screen
        this.workSurface = screen.copy()

    def addObject(this, obj, x, y, alpha):
        this.objects.append(Renderable(obj, x, y, alpha))

    def addShader(this, shader):
        this.shaders.append(shader)

    def update(this):

        for renderable in objects:
            renderable.get_object().draw(this.screen, renderable.get_x(), renderable.get_y())


        shaderSurface = this.screen.copy()
        for shader in this.shaders:
            shaderSurface = shader.apply(shaderSurface)
        this.screen.blit(shaderSurface, (0,0))