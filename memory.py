# v3 

# this code is for the game Memory

import pygame, random, time

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board_size = 4
      self.board = []
      self.tiles_to_compare = []
      self.set_up_board()
      self.score = 0
      
   def set_up_board(self):
      # set up the board 
      Tile.set_surface(self.surface)
      self.tile_images()
      tile_size = self.surface.get_height() // self.board_size
      index=0
      for row_number in range(0, self.board_size):
         row = []
         for column_number in range(0, self.board_size):
            x = column_number * tile_size
            y = row_number * tile_size
            tile = Tile(x, y, tile_size, tile_size, self.image_list[index], self.tiles_to_compare)
            index+=1
            row.append(tile)
         self.board.append(row)
          
   def tile_images(self):
      # load all the tile images and create a list of images
      number_of_images = 9
      images = []
      for i in range(1, number_of_images):
         images.append(pygame.image.load("image"+str(i)+".bmp"))
      self.image_list = images + images
      random.shuffle(self.image_list)     

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_event(event.pos)         
   
   def handle_mouse_event(self, pos):
      # check if the (x, y) of mouse is inside this tile
      # and change the tile's content accordingly  
      
      if len(self.tiles_to_compare) < 2:
         for row in self.board:
            for tile in row:
               if tile.select(pos):
                  self.tiles_to_compare.append(tile)
 
                         
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      for row in self.board:
         for tile in row:
            tile.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display  

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.score = pygame.time.get_ticks() // 1000
      if len(self.tiles_to_compare) == 2:
         tile1, tile2 = self.tiles_to_compare
         if tile1 != tile2:
            for tile in self.tiles_to_compare:
               tile.flip_tile()
         time.sleep(0.5)
         self.tiles_to_compare.clear()
         
            
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      for row in self.board:
         for tile in row:
            if not tile.is_exposed():
               self.continue_game = True               
               return            
      self.continue_game = False
   
   def draw_score(self):
      # Draw the time since the game began as a score
      # - self is the Game to draw for. 
      
      score_string = str(self.score)    
      score_font = pygame.font.SysFont('', 85)
      score_fg_color = pygame.Color('white')
      score_image = score_font.render(score_string, True, score_fg_color)
      score_location = self.surface.get_width() - score_image.get_width()
      self.surface.blit(score_image, (score_location,0))          


class Tile:
   # An object in this class represents a TTT Tile 
   
   border_width = 3
   fg_color = pygame.Color('black')
   surface = None
   
   @classmethod
   def set_surface(cls, surface):
      cls.surface = surface
   
   def __init__(self, x, y, width, height, image, tiles_to_compare):
      # Initialize a Tile. 
      # - self is the Dot to initialize
      # - ...

      self.rect = pygame.Rect(x, y, width, height)
      self.location = (self.rect.x, self.rect.y)
      self.new_image = image
      self.start_image = pygame.image.load('image0.bmp')
      self.content = self.start_image
      self.tiles_clicked = tiles_to_compare
      
   def draw(self):
      # draw content
      
      pygame.draw.rect(Tile.surface, Tile.fg_color, self.rect, Tile.border_width)
      self.surface.blit(self.content, self.location)   
      
   def select(self, pos):
      # checks if mouse click occurs inside a tile
      # if the tile is unexposed, the image on the tile is changed
      
      valid_move = False
      if self.rect.collidepoint(pos):
         if self.content == self.start_image:
            self.content = self.new_image
            valid_move = True
      return valid_move  
   
   def is_exposed(self):
      # Checks to see if all tiles are exposed
      
      matching_content = False
      if self.content == self.new_image:
         matching_content = True
      return matching_content
   
   def __eq__(self, other):
      # compares the two tiles and returns if the images match or not
      match = False
      if self.content == other.content:
         match = True
      return match
   
   def flip_tile(self):
      # changes the tile image back to start_image
      
      self.content = self.start_image
      
main()