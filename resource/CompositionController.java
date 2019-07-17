package com.septemberhxtest.mcomposition.controller;

import com.septemberhx.mclient.annotation.MApiFunction;
import com.septemberhx.mclient.annotation.MFunctionType;
import com.septemberhx.mclient.base.MObject;
import com.septemberhx.mclient.base.MResponse;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CompositionController extends MObject {{

    {definition}

    @RequestMapping(path = "{path}", method = RequestMethod.POST)
    @MApiFunction
    public MResponse test(@RequestBody MResponse body) {{
        {body}
    }}
}}
