'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY._0:
        world.next = True
    elif symbol == KEY.G:
        add_agent()
    elif symbol == KEY.T:
        count = 0
        while count < 10:
            count += 1
            add_agent()
    # LAB 06 TASK 1: Reset all paths to new random ones
    elif symbol == KEY.O:
        for agent in world.agents:
            agent.randomise_path()
    # Toggle debug force line info on the agent
    elif symbol == KEY.B:
        Agent.show_info = not Agent.show_info
    elif symbol == KEY.I:
        Agent.loop = not Agent.loop
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    #SCALE
    elif symbol == KEY.Q:
        if Agent.floatScale > 1.0:
            Agent.floatScale -= 1.0
    elif symbol == KEY.W:
        Agent.floatScale += 1.0
    #MAX SPEED
    elif symbol == KEY.E:
        if Agent.max_speed > 5.0:
            Agent.max_speed -= 5.0
    elif symbol == KEY.R:
        Agent.max_speed += 5.0
    #MAX FORCE
    elif symbol == KEY.A:
        if Agent.max_force > 5.0:
            Agent.max_force -= 5.0
    elif symbol == KEY.S:
        Agent.max_force += 5.0
    #MASS
    elif symbol == KEY.D:
        if Agent.mass > 0.1:
            Agent.mass -= 0.1
    elif symbol == KEY.F:
            Agent.mass += 0.1
    #FRICTION
    elif symbol == KEY.Z:
        if Agent.friction > 0.01:
            Agent.friction -= 0.01
    elif symbol == KEY.X:
        Agent.friction += 0.01
    #PANIC DISTANCE
    elif symbol == KEY.C:
        if Agent.panicDist > 5:
            Agent.panicDist -= 5
    elif symbol == KEY.V:
        Agent.panicDist += 5
    #WAYPOINT THRESHOLD
    elif symbol == KEY.Y:
        if Agent.waypoint_threshold > 5:
            Agent.waypoint_threshold -= 5
    elif symbol == KEY.U:
        Agent.waypoint_threshold += 5
    #WANDER DISTANCE
    elif symbol == KEY.H:
        if Agent.wander_dist > 0.25:
                Agent.wander_dist -= 0.25
    elif symbol == KEY.J:
        Agent.wander_dist += 0.25
    #WANDER RADIUS
    elif symbol == KEY.K:
        if Agent.wander_radius > 0.25:
            Agent.wander_radius -= 0.25
    elif symbol == KEY.L:
        Agent.wander_radius += 0.25
    #WANDER JITTER
    elif symbol == KEY.N:
        if Agent.wander_jitter > 1:
            Agent.wander_jitter -= 1
    elif symbol == KEY.M:
        Agent.wander_jitter += 1

def add_agent():
    newAgent = Agent(world.hunter.mode)
    world.agents.append(newAgent)
    world.hunter = newAgent

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy
def render_stats(world):
    egi.text_color((1.0, 1.0, 1.0, 1))
    depthy = -40
    egi.text_at_pos(10, depthy, '(Q/W) Game Scale = ' + str(Agent.floatScale))
    egi.text_at_pos(10, depthy-20, '(E/R) Max Speed = ' + str(Agent.max_speed))
    egi.text_at_pos(10, depthy-40, '(A/S) Max Force = ' + str(Agent.max_force))
    egi.text_at_pos(10, depthy-60, '(D/F) Mass = ' + str(Agent.mass))
    egi.text_at_pos(10, depthy-80, '(Z/X) Friction = ' + str(Agent.friction))
    egi.text_at_pos(10, depthy-100, '(C/V) Panic Distance = ' + str(Agent.panicDist))
    egi.text_at_pos(10, depthy-130, '(Y/U) Waypoint Threshold = ' + str(Agent.waypoint_threshold))
    egi.text_at_pos(10, depthy-150, '(I) Waypoint Loop = ' + str(Agent.loop))
    egi.text_at_pos(10, depthy-170, '(O) Randomize Path')
    egi.text_at_pos(10, depthy-200, '(H/J) Wander Distance = ' + str(Agent.wander_dist))
    egi.text_at_pos(10, depthy-220, '(K/L) Wander radius = ' + str(Agent.wander_radius))
    egi.text_at_pos(10, depthy-240, '(N/M) Wander jitter = ' + str(Agent.wander_jitter))
    egi.text_at_pos(10, depthy-270, '(B) Show agent info')
    egi.text_at_pos(10, depthy-290, '(P) Pause')
    egi.text_at_pos(10, depthy-310, '(0) Next frame (while paused)')


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=1000, height=1000, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add two agents (first one is done manually so default agent values are entered)
    newAgent = Agent('seek', world)
    world.agents.append(newAgent)
    world.hunter = newAgent
    add_agent()
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        render_stats(world)
        fps_display.draw()
        # swap the double buffer
        win.flip()

