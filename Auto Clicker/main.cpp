#if defined(UNICODE) && !defined(_UNICODE)
    #define _UNICODE
#elif defined(_UNICODE) && !defined(UNICODE)
    #define UNICODE
#endif

#include <tchar.h>
#include <windows.h>
#include <iostream>
#include <vector>
#include <stdio.h>

/*  Declare Windows procedure  */
LRESULT CALLBACK WindowProcedure (HWND, UINT, WPARAM, LPARAM);
HWND textbox, capBtn, startBtn, clrBtn;
POINT cursorLoc;
std::vector<POINT> allLocs;
int numRuns = 0;
/*  Make the class name into a global variable  */
TCHAR szClassName[ ] = _T("CodeBlocksWindowsApp");

int WINAPI WinMain (HINSTANCE hThisInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR lpszArgument,
                     int nCmdShow)
{
    HWND hwnd;               /* This is the handle for our window */
    MSG messages;            /* Here messages to the application are saved */
    WNDCLASSEX wincl;        /* Data structure for the windowclass */

    /* The Window structure */
    wincl.hInstance = hThisInstance;
    wincl.lpszClassName = szClassName;
    wincl.lpfnWndProc = WindowProcedure;      /* This function is called by windows */
    wincl.style = CS_DBLCLKS;                 /* Catch double-clicks */
    wincl.cbSize = sizeof (WNDCLASSEX);

    /* Use default icon and mouse-pointer */
    wincl.hIcon = LoadIcon (NULL, IDI_APPLICATION);
    wincl.hIconSm = LoadIcon (NULL, IDI_APPLICATION);
    wincl.hCursor = LoadCursor (NULL, IDC_ARROW);
    wincl.lpszMenuName = NULL;                 /* No menu */
    wincl.cbClsExtra = 0;                      /* No extra bytes after the window class */
    wincl.cbWndExtra = 0;                      /* structure or the window instance */
    /* Use Windows's default colour as the background of the window */
    wincl.hbrBackground = (HBRUSH) COLOR_BACKGROUND;

    /* Register the window class, and if it fails quit the program */
    if (!RegisterClassEx (&wincl))
        return 0;

    /* The class is registered, let's create the program*/
    hwnd = CreateWindowEx (
           0,                   /* Extended possibilites for variation */
           szClassName,         /* Classname */
           _T("Auto Clicker"),       /* Title Text */
           WS_MINIMIZEBOX | WS_SYSMENU, /* default window */
           CW_USEDEFAULT,       /* Windows decides the position */
           CW_USEDEFAULT,       /* where the window ends up on the screen */
           544,                 /* The programs width */
           375,                 /* and height in pixels */
           HWND_DESKTOP,        /* The window is a child-window to desktop */
           NULL,                /* No menu */
           hThisInstance,       /* Program Instance handler */
           NULL                 /* No Window Creation data */
           );

    /* Make the window visible on the screen */
    ShowWindow (hwnd, nCmdShow);

    /* Run the message loop. It will run until GetMessage() returns 0 */
    while (GetMessage (&messages, NULL, 0, 0))
    {
        /* Translate virtual-key messages into character messages */
        TranslateMessage(&messages);
        /* Send message to WindowProcedure */
        DispatchMessage(&messages);
    }

    /* The program return-value is 0 - The value that PostQuitMessage() gave */
    return messages.wParam;
}


/*  This function is called by the Windows function DispatchMessage()  */

LRESULT CALLBACK WindowProcedure (HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)                  /* handle the messages */
    {
        case WM_CREATE:                 /*when window is created*/
            textbox = CreateWindow("EDIT",
                                     "1",
                                     WS_VISIBLE | WS_CHILD | WS_BORDER,
                                     20,20,300,30,
                                     hwnd,
                                     NULL, NULL, NULL);
            startBtn = CreateWindow("BUTTON",
                                  "Start",
                                  WS_VISIBLE | WS_CHILD | WS_BORDER,
                                  20,70,200,40,
                                  hwnd,
                                  (HMENU) 2,NULL,NULL);
            capBtn = CreateWindow("BUTTON",
                                  "Capture Mouse Coords",
                                  WS_VISIBLE | WS_CHILD | WS_BORDER,
                                  240,70,200,40,
                                  hwnd,
                                  (HMENU) 1,NULL,NULL);
             clrBtn = CreateWindow("BUTTON",
                                  "Clear Clicks",
                                  WS_VISIBLE | WS_CHILD | WS_BORDER,
                                  20,130,200,40,
                                  hwnd,
                                  (HMENU) 3,NULL,NULL);
        break;

        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
                //capture/add current mouse coords
                case 1:
                {
                    BOOL result = GetCursorPos(&cursorLoc);
                    if(result)
                    {
                        allLocs.push_back(cursorLoc);
                        std::cout << cursorLoc.x <<',' << cursorLoc.y<< std::endl;
                    }

                }
                break;
                //move mouse to stored coords
                case 2:
                {
                    //loop through all set coords
                    for(int i = 0; i < allLocs.size(); ++i){
                        SetCursorPos(allLocs.at(i).x, allLocs.at(i).y);
                        Sleep(1000);
                    }
                }
                break;
                //clear stored coords
                case 3:
                {
                    allLocs.resize(0);
                }
                break;
            }
            break;

        case WM_DESTROY:
            PostQuitMessage (0);       /* send a WM_QUIT to the message queue */
            break;
        default:                      /* for messages that we don't deal with */
            return DefWindowProc (hwnd, message, wParam, lParam);
    }

    return 0;
}
