"""Supplied Pygame view. Do not submit or edit for credit. Import is side-effect free."""
import argparse
import multiprocessing as mp
import queue
import time


def _ai_job(controller, output):
    try:
        move = controller.ai_move()
        output.put(('ok', controller.state, move))
    except Exception as error:
        output.put(('error', type(error).__name__ + ': ' + str(error)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=4, choices=range(3,9))
    parser.add_argument('--depth', type=int, default=2, choices=range(1,5))
    parser.add_argument('--algorithm', choices=('minimax','negamax'), default='minimax')
    parser.add_argument('--human', choices=('O','X'), default='O')
    parser.add_argument('--smoke', action='store_true', help='render a short scripted sequence and exit')
    parser.add_argument('--screenshot', help='save the final rendered frame as PNG')
    args = parser.parse_args()
    import pygame
    from game_controller import GameController
    pygame.init()
    screen = pygame.display.set_mode((840,820))
    pygame.display.set_caption('CSE 5120 | Scored tic-tac-toe')
    font = pygame.font.Font(None,27)
    title_font = pygame.font.Font(None,40)
    clock = pygame.time.Clock()
    controller = GameController(args.size,args.human,args.algorithm,args.depth)
    job, channel, started = None,None,0
    message = 'You move first. Make a prediction, then click an empty cell.'
    frame = 0

    def text(value,xy,color=(30,40,60),title=False):
        screen.blit((title_font if title else font).render(value,True,color),xy)

    def stop_job():
        nonlocal job,channel
        if job is not None:
            if job.is_alive(): job.terminate()
            job.join(timeout=1)
            job.close()
        if channel is not None: channel.close()
        job,channel = None,None

    def new_game(size=None,human=None,algorithm=None,depth=None):
        nonlocal controller,message
        stop_job()
        controller = GameController(size or controller.size,human or controller.human_symbol,
                                    algorithm or controller.algorithm,depth or controller.depth)
        message='New game. You move first.'

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running=False
                    elif event.key == pygame.K_r: new_game()
                    elif event.unicode in ('3','4','5'): new_game(size=int(event.unicode))
                    elif event.key in (pygame.K_o,pygame.K_x): new_game(human=event.unicode.upper())
                    elif event.key == pygame.K_m: new_game(algorithm='minimax')
                    elif event.key == pygame.K_n: new_game(algorithm='negamax')
                    elif event.key == pygame.K_UP: new_game(depth=min(4,controller.depth+1))
                    elif event.key == pygame.K_DOWN: new_game(depth=max(1,controller.depth-1))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and job is None:
                    x,y = event.pos
                    if 120 <= x < 720 and 145 <= y < 745:
                        col=(x-120)*controller.size//600
                        row=(y-145)*controller.size//600
                        if controller.human_move(row,col): message='Human move accepted.'
            if args.smoke and frame == 1:
                controller.human_move(0,0)
                controller.ai_move()
            status=controller.status()
            if not args.smoke and job is None and not status['terminal'] and status['turn'] != controller.human_symbol:
                channel=mp.get_context('spawn').Queue()
                job=mp.get_context('spawn').Process(target=_ai_job,args=(controller,channel),daemon=True)
                job.start();started=time.monotonic();message='AI is searching. Reset or Escape remains available.'
            if job is not None:
                try:
                    result=channel.get_nowait()
                except queue.Empty:
                    result=None
                if result is not None:
                    stop_job()
                    if result[0]=='ok': controller.state=result[1];message='AI move: '+str(result[2])
                    else:
                        message=result[1][:95]
                        # Stop automatic retries until the player resets.
                        screen.fill((245,247,251));text(message,(25,100));pygame.display.flip()
                        raise RuntimeError(message)
                elif time.monotonic()-started > 15:
                    stop_job();new_game(depth=max(1,controller.depth-1))
                    message='Search exceeded 15 seconds. Reset with a lower depth.'
            status=controller.status()
            screen.fill((245,247,251))
            text('Scored tic-tac-toe',(25,18),title=True)
            text('You: %s   AI: %s   %s   depth %d moves' %
                 (controller.human_symbol,'X' if controller.human_symbol=='O' else 'O',controller.algorithm,controller.depth),(25,62))
            text('3 / 4 / 5: size    O / X: symbol    M / N: algorithm    Up / Down: depth',(25,95))
            cell=600/controller.size
            for row in range(controller.size):
                for col in range(controller.size):
                    rect=pygame.Rect(120+col*cell,145+row*cell,cell,cell)
                    pygame.draw.rect(screen,(255,255,255),rect)
                    pygame.draw.rect(screen,(165,178,193),rect,2)
                    value=controller.state.board_state[row][col]
                    pad=max(10,int(cell*0.23))
                    if value==1: pygame.draw.circle(screen,(24,106,166),rect.center,int(cell/2)-pad,5)
                    elif value==-1:
                        pygame.draw.line(screen,(170,63,57),(rect.left+pad,rect.top+pad),(rect.right-pad,rect.bottom-pad),5)
                        pygame.draw.line(screen,(170,63,57),(rect.right-pad,rect.top+pad),(rect.left+pad,rect.bottom-pad),5)
            label=('Winner: '+status['winner']) if status['terminal'] else ('Turn: '+status['turn'])
            text('Triplets  O: %d   X: %d     %s     R: reset    Esc: quit' % (status['O'],status['X'],label),(25,760))
            text(message,(25,791))
            pygame.display.flip()
            frame+=1
            if args.smoke and frame>=3:
                if args.screenshot: pygame.image.save(screen,args.screenshot)
                running=False
            clock.tick(30)
    finally:
        stop_job()
        pygame.quit()


if __name__ == '__main__':
    mp.freeze_support()
    main()
