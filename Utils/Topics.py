def generate_topic():
    # Define the topic content
    return """
    topic: ~ContextAwareTopic()
    language: spe
    concept:(context) [SpiritualTask MusicTask StoryTask ExerciseTask DrugTask BlankTask]

    u: (SpiritualTask.hola) hola     
    u: (SpiritualTask.TurnOffLight) a
    u: (SpiritualTask.AdjustBrightness)  a

    u: (MusicTask.hola) adios
    u: (MusicTask.PauseMusic) a
    u: (MusicTask.SkipTrack) a

    u: (StoryTask.hola)  sapo
    u: (StoryTask.PauseMusic) a
    u: (StoryTask.SkipTrack) a

    u: (ExerciseTask.hola)  test
    u: (ExerciseTask.PauseMusic) a
    u: (ExerciseTask.SkipTrack) a

    u: (DrugTask.hola) test2
    u: (DrugTask.PauseMusic) a
    u: (DrugTask.SkipTrack) a

    u: (BlankTask.hola) nada
    """
    
def change_context(dialog_service, new_context):
    dialog_service.setConcept("context", new_context)