use std::thread::current;

use macroquad::{
    color::Color,
    math::{vec2, Rect, Vec2},
    shapes::draw_line,
    texture::{draw_texture_ex, DrawTextureParams, Texture2D},
    window::{screen_height, screen_width},
};
use macroquad_platformer::{Actor, World};
use macroquad_tiled::Map;

use crate::enemy::Enemy;

#[derive(Debug, Eq, PartialEq, Clone, Copy)]
pub enum CharacterActionState {
    Idle,
    Attacking,
    Damaging,
    Projected,
}
#[derive(Debug, PartialEq, Clone)]

/*
    Character
*/

pub struct Character 
{
    // Game values
    pub hp: u8,
    pub mp: u8, // Unused
    pub turn_angle: u32, 
    pub attack_damage: u8,
    // Drawing
    pub sprite: String,

    // Animation
    pub action: CharacterActionState,
    pub action_frame: u32,
    pub attack_selector: u32,

    // Colliding
    pub collider: Actor,
    pub attack_collider: Actor,

    // Sprite movement
    pub knocked_back: bool,
    pub knockback_frames: u32,
    pub next_final_pos: Vec2,
    pub sprite_displacement: Vec2,
    pub last_frame_smoothed: bool,
    pub move_ordered: bool,
}

impl Character 
{
    // Attacks what's in front of you
    pub fn attack_one(&mut self, enemy: &mut Character, world: &mut World) 
    {
        let attack_draw_vector = vec2(
            (self.turn_angle as f32).to_radians().sin(),
            (self.turn_angle as f32).to_radians().cos(),
        );

        
        for point in 0..3
        {
            let attack_position = world.actor_pos(self.collider) + (attack_draw_vector * point as f32);
            
            let position = world.actor_pos(enemy.collider);
            // println!("Enemy at : {:?} | attack at {:?}", position, attack_position);
            

            if position == attack_position {
                // println!("Damage taken");
                enemy.take_damage(world, self);
            }
        }

        return;
    }

    pub fn attack(&mut self, enemies: &mut Vec<Enemy>, world: &mut World) 
    {
        if self.action == CharacterActionState::Attacking
        {
            return
        }

        let attack_draw_vector = vec2(
            (self.turn_angle as f32).to_radians().sin(),
            (self.turn_angle as f32).to_radians().cos(),
        );

        
        for point in 0..3
        {
            let attack_position = world.actor_pos(self.collider) + (attack_draw_vector * point as f32);
            
            for enemy in enemies.iter_mut() 
            {
                let position = world.actor_pos(enemy.char.collider);
                // ("Enemy at : {:?} | attack at {:?}", position, attack_position);
                
    
                if position == attack_position {
                    // println!("Damage taken");
                    enemy.char.take_damage(world, self);
                }
            }
        }


        return;
    }

    pub fn take_damage(&mut self, world: &mut World, from: &Character) 
    {
        if self.hp <= 0
        {
            return;            
        }

        self.hp -= from.attack_damage as u8;

        self.knocked_back = true;
        
        if !self.sprite.ends_with("_Damaged")
        {
            if !self.sprite.contains("Foam")
            {
                self.sprite = format!("{}_Damaged", self.sprite);
            }
        }
       
        let self_position = world.actor_pos(self.collider);

        let mut attack_back_vector = world.actor_pos(from.collider) - self_position;
        attack_back_vector.x = attack_back_vector.x * 2.;
        attack_back_vector.y = attack_back_vector.y * 2.;

        let next_final_pos = self_position - (attack_back_vector);

        // Avoid colliding into an edge and just don't knockback
        if !world.solid_at(next_final_pos) 
        {
            // println!("No solid at {:?}", next_final_pos);
            self.next_final_pos = next_final_pos;
        } else {
            self.knocked_back = false;
        }
    }

    // Guess why we have to handle this shit ourselves ? 
    // Because the macroquad dev decided that muh we can only move 1 by 1.
    // Seriously dude ?
    pub fn position_smoother(&mut self, world: &mut World) 
    {
        const THRESHOLD: f32 = 1.0;
        const MOVE_AMOUNT: f32 = 1.0;

        // Adjust sprite displacement if a move was ordered last frame
        if self.move_ordered 
        {
            // println!("Move ordered!");
            
            let x_movement = self.sprite_displacement.x.signum() * MOVE_AMOUNT.min(self.sprite_displacement.x.abs());
            let y_movement = self.sprite_displacement.y.signum() * MOVE_AMOUNT.min(self.sprite_displacement.y.abs());

            self.sprite_displacement.x -= x_movement;
            self.sprite_displacement.y -= y_movement;
            self.move_ordered = false;
        }

        // Check if we need to order a world move for the next frame
        // The idea is that if we applied a sprite displacement of more than 1.
        // We have to move on the next square
        let move_x = self.sprite_displacement.x.abs() > THRESHOLD;
        let move_y = self.sprite_displacement.y.abs() > THRESHOLD;

        
        if move_x || move_y 
        {
            let x_movement = self.sprite_displacement.x.signum() * MOVE_AMOUNT.min(self.sprite_displacement.x.abs());
            let y_movement = self.sprite_displacement.y.signum() * MOVE_AMOUNT.min(self.sprite_displacement.y.abs());

            // Move the world
            // Why is the logic this way ?
            // Because thanks to the macroquad developer, the world moves on THE NEXT FRAME JFEIOZJGOZEGZEOG
            world.move_h(self.collider, x_movement);
            world.move_v(self.collider, y_movement);

            self.move_ordered = true;
        }

    }

    /// Knockback
    pub fn apply_displacement(&mut self, world: &mut World) 
    {
        if !self.knocked_back 
        {
            self.knockback_frames = 0;
            return;
        }

        self.knockback_frames += 1;

        if self.knockback_frames >= 100
        {
            self.knocked_back = false;
            self.sprite_displacement = vec2(0., 0.);
            self.knocked_back = false;
            if self.sprite.contains("_Damaged") 
            {
                self.sprite = self.sprite.split("_Damaged").nth(0).unwrap().to_string();
            }
            return;
        }

        let self_position = world.actor_pos(self.collider);

        // Will happen on next iteration when the displacement is < 0.3
        if self_position == self.next_final_pos 
        {
            self.sprite_displacement = vec2(0., 0.);
            self.knocked_back = false;
            if self.sprite.contains("_Damaged") 
            {
                self.sprite = self.sprite.split("_Damaged").nth(0).unwrap().to_string();
            }
            return;
        }

        // println!(
        //     "self pos : {:?}, final pos : {:?}, displacement {:?}",
        //     self_position, self.next_final_pos, self.sprite_displacement
        // );

        let remaining_displacement = self.next_final_pos - (self_position + self.sprite_displacement);

        let abs_displacement = remaining_displacement.abs();

        // println!("Remaining displacement : {:?}", abs_displacement);

        if abs_displacement.x < 0.3 && abs_displacement.y < 0.3 
        {
            // println!("Ended displacement");

            world.move_h(self.collider, remaining_displacement.x);
            world.move_v(self.collider, remaining_displacement.y);
            self.sprite_displacement = vec2(0., 0.);

            return;
        }

        const MAX_DISPLACEMENT: f32 = 0.4;
        let mut new_displacement = vec2(0., 0.);

        if abs_displacement.x > 0. 
        {
            new_displacement.x = remaining_displacement.x.signum() * MAX_DISPLACEMENT.min(abs_displacement.x);
        }

        if abs_displacement.y > 0. 
        {
            new_displacement.y = remaining_displacement.y.signum() * MAX_DISPLACEMENT.min(abs_displacement.y);
        }

        self.sprite_displacement += new_displacement;

    }

    pub fn draw_character(&mut self, map: &Map, pos: Vec2) 
    {
        let multiplier = {
            match self.turn_angle {
                90 => 1,
                180 => 1,
                0 => 1,
                _ => 1,
            }
        };

        let mut current_sprite = 0;

        // Torch doesn't have the same size as Wizar
        // Code is dirty, don't care
        if self.sprite.contains("Torch")
        {
            current_sprite = 
            {
                if self.action == CharacterActionState::Idle 
                {
                    if self.action_frame >= 5
                    {
                        0
                    }
                    else {
                        self.action_frame + 1
                    }
                }
                else if self.action == CharacterActionState::Attacking 
                {
                    if self.action_frame < 14
                    {
                        14
                    }
                    else if self.action_frame >= 19
                    {
                        self.action = CharacterActionState::Damaging;
                        0
                    }
                    else {
                        self.action_frame + 1
                    }
                    
                }
                else {
                    0
                }
            };

        }
        else {
                    // Current sprite for animation
        current_sprite = {
            if self.action == CharacterActionState::Idle 
            {
                if self.action_frame >= 5 {
                    self.attack_selector = 0;
                    0
                } else {
                    self.action_frame + 1
                }
            } else if self.action == CharacterActionState::Attacking 
            {
                if self.action_frame < (12 * multiplier + self.attack_selector) {
                    12 * multiplier + self.attack_selector
                } else if self.action_frame >= (12 * multiplier + 5 + self.attack_selector) {
                    self.attack_selector = {
                        if self.attack_selector == 0 {
                            0
                        } else {
                            0
                        }
                    };
                    self.action = CharacterActionState::Damaging;

                    0
                } else {
                    {
                        self.action_frame + 1
                    }
                }
            } else {
                0
            }
        };
        }


        let sprite_mod = match self.turn_angle {
            270 => -1.,
            _ => 1.,
        };

        self.action_frame = current_sprite;

        map.spr(
            &self.sprite,
            current_sprite,
            Rect::new(
                // Position is top left corner
                // Apply sprite mod (x direction) on the middle of the image (3 / 2)
                pos.x - (1.5 * sprite_mod) + self.sprite_displacement.x,
                pos.y - 2. + self.sprite_displacement.y,
                3. * sprite_mod,
                4.,
            ),
        );
    }

    
}
