use macroquad::{color::Color, shapes::draw_rectangle, text::draw_text};

#[derive(Debug, Eq, PartialEq, Clone)]
pub struct QuestLog
{
    pub quests: Vec<Objective>,
}

/// Handles the questing.
impl QuestLog
{
    pub fn init(&mut self)
    {
        let quest_0 = Objective::new("Kill the nasty goblins hanging out by your yard [ ]");
        let quest_1 = Objective::new("????? [ ]");
        let quest_2 = Objective::new("Don't touch the sand for more than 10s [ ]");

        self.quests.push(quest_0);
        self.quests.push(quest_1);
        self.quests.push(quest_2);
    }

    pub fn render(&self, sw: f32, sh: f32)
    {
        draw_rectangle(5., 5., sw - 5., sh - 5., Color::from_rgba(0, 0, 0, 50));
        
        let mut y_offset = 0.;

        for quest in &self.quests
        {
            draw_text(&quest.description, 10., 30. + y_offset, 30., Color::from_rgba(255, 255, 255, 255));
            y_offset += 30.
        }
    }

    pub fn quests_done(&mut self) -> bool
    {
        for quest in &self.quests
        {
            if !quest.complete
            {
                return false
            }
        }

        return true
    }

}

#[derive(Debug, Eq, PartialEq, Clone)]
pub struct Objective
{
    pub description: String,
    pub complete: bool
}

impl Objective
{
    pub fn new(description : &str) -> Objective
    {
        Objective
        {
            description: description.to_string(),
            complete: false
        }
    }

    pub fn mark_complete(&mut self)
    {
        if self.complete
        {
            return;
        }
        
        self.description.pop().unwrap();
        self.description.pop().unwrap();

        self.description.push('X');
        self.description.push(']');
        self.complete = true;
        
    }
}