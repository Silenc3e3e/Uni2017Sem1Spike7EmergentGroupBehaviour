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
    if symbol == KEY.G:
        add_agent()
    elif symbol == KEY.T:
        count = 0
        while count < 10:
            count += 1
            add_agent()
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    
    #displaystuff
    elif symbol == KEY.Y:
        Agent.show_info = not Agent.show_info
    elif symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY.O:
        world.next = True
    elif symbol == KEY.H:
        world.inputgroup += 1
        if world.inputgroup > 3:
            world.inputgroup = 0
    elif not world.inputgroup == 0:
        if world.inputgroup == 1:
            #SCALE
            if symbol == KEY.Q:
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
        elif world.inputgroup == 2:
            #WAYPOINT THRESHOLD
            if symbol == KEY.Q:
                if Agent.waypoint_threshold > 5:
                    Agent.waypoint_threshold -= 5
            elif symbol == KEY.W:
                Agent.waypoint_threshold += 5
            #WAYPOINT LOOP
            elif symbol == KEY.A:
                Agent.loop = not Agent.loop
            # LAB 06 TASK 1: Reset all paths to new random ones
            #RANDOMIZE PATH
            elif symbol == KEY.S:
                for agent in world.agents:
                    agent.randomise_path()
        elif world.inputgroup == 3:
            #WANDER DISTANCE
            if symbol == KEY.Q:
                if Agent.wander_dist > 0.25:
                        Agent.wander_dist -= 0.25
            elif symbol == KEY.W:
                Agent.wander_dist += 0.25
            #WANDER RADIUS
            elif symbol == KEY.E:
                if Agent.wander_radius > 0.25:
                    Agent.wander_radius -= 0.25
            elif symbol == KEY.R:
                Agent.wander_radius += 0.25
            #WANDER JITTER
            elif symbol == KEY.A:
                if Agent.wander_jitter > 1:
                    Agent.wander_jitter -= 1
            elif symbol == KEY.S:
                Agent.wander_jitter += 1
   
    

def add_agent():
    newAgent = Agent(world.hunter.mode)
    world.agents.append(newAgent)
    world.hunter = newAgent

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy
def render_stats(world):
    if not world.inputgroup == 0:
        egi.text_color((1.0, 1.0, 1.0, 1))
        depthy = -40
        if world.inputgroup == 1:
            egi.text_at_pos(10, depthy, '(Q/W) Game Scale = ' + str(Agent.floatScale))
            egi.text_at_pos(10, depthy-20, '(E/R) Max Speed = ' + str(Agent.max_speed))
            egi.text_at_pos(10, depthy-40, '(A/S) Max Force = ' + str(Agent.max_force))
            egi.text_at_pos(10, depthy-60, '(D/F) Mass = ' + str(Agent.mass))
            egi.text_at_pos(10, depthy-80, '(Z/X) Friction = ' + str(Agent.friction))
            egi.text_at_pos(10, depthy-100, '(C/V) Panic Distance = ' + str(Agent.panicDist))
        elif world.inputgroup == 2:
            egi.text_at_pos(10, depthy, '(Q/W) Waypoint Threshold = ' + str(Agent.waypoint_threshold))
            egi.text_at_pos(10, depthy-20, '(A) Waypoint Loop = ' + str(Agent.loop))
            egi.text_at_pos(10, depthy-40, '(S) Randomize Path')
        elif world.inputgroup == 3:
            egi.text_at_pos(10, depthy, '(Q/W) Wander Distance = ' + str(Agent.wander_dist))
            egi.text_at_pos(10, depthy-20, '(E/R) Wander radius = ' + str(Agent.wander_radius))
            egi.text_at_pos(10, depthy-40, '(A/S) Wander jitter = ' + str(Agent.wander_jitter))
        egi.text_at_pos(10, depthy-130, '(Y) Show agent info')
        egi.text_at_pos(10, depthy-150, '(P) Pause')
        egi.text_at_pos(10, depthy-170, '(O) Next frame (while paused)')
        egi.text_at_pos(10, depthy-190, '(H) Flick through menu')


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

