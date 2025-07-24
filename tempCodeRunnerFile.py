r = 0
while not level.scaled:
    # update listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # backgorund
    screen.fill(C.white)
    text = font.render("Loading assets...", True, (0, 0, 0))
    screen.blit(
        text,
        (
            (screen.get_width() / 2) - 200,
            (screen.get_height() / 2) - 100,
        ),
    )
    r += 1
    draw(
        screen,
        screen.get_width() / 2,
        screen.get_height() / 2,
        r,
        l1,
        l2,
        l3,
        l4,
        l5,
        2.5,
    )
    pygame.display.update()