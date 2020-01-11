package com.septemberhx.mcomposition;

import com.septemberhx.mclient.annotation.MApiFunction;
import com.septemberhx.mclient.annotation.MRestApiType;
import com.septemberhx.mclient.annotation.MFunctionType;
import com.septemberhx.mclient.base.MObject;
import com.septemberhx.common.base.MResponse;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CompositionController extends MObject {{

    {definition}

    @RequestMapping(path = "{path}", method = RequestMethod.POST)
    @MApiFunction
    @MRestApiType
    public MResponse test(@RequestBody MResponse body) {{
        {body}
    }}
}}
