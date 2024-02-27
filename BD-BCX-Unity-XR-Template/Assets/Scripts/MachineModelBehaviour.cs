using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MachineModelBehaviour : MonoBehaviour
{

    public GameObject beltHighlight;

    public GameObject pistonHead;

    public bool highlightBelt;

    public bool extendPiston;

    public int lastHighlightSwitch;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void FixedUpdate()
    {
        if (beltHighlight)
        {
            lastHighlightSwitch++;
            if(lastHighlightSwitch > 10)
            {
                beltHighlight.SetActive(!beltHighlight.activeSelf);
                lastHighlightSwitch = 0;
            }
        }
    }
}
