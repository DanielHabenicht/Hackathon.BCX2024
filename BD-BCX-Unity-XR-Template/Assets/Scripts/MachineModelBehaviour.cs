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

    public Vector3 extendedPosition;

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
        if (highlightBelt)
        {
            lastHighlightSwitch++;
            if(lastHighlightSwitch > 10)
            {
                beltHighlight.SetActive(!beltHighlight.activeSelf);
                lastHighlightSwitch = 0;
            }
        }

            if (extendPiston)
            {
                if(pistonHead.transform.localPosition.z < extendedPosition.z)
                {
                    pistonHead.transform.SetLocalPositionAndRotation(pistonHead.transform.localPosition + extendedPosition / 20, Quaternion.identity);
                }
            }
            else
            {
                if(pistonHead.transform.localPosition.z > 0)
                {
                    pistonHead.transform.SetLocalPositionAndRotation(pistonHead.transform.localPosition - extendedPosition / 20, Quaternion.identity);
                }
            }
        
    }
}
