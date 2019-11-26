package {package_name}

import org.springframework.core.DefaultParameterNameDiscoverer;
import org.springframework.web.bind.annotation.*;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
public class MController {{

    {mobject_class} mObject = new {mobject_class}();

    @ResponseBody
    @RequestMapping(value = {{{url_values}}}, method = RequestMethod.POST)
    public Object fun1(@RequestBody Map<String, Object> jsonObject) {{
        System.out.println(jsonObject);
        String methodName = (String)jsonObject.get("method");
        Map<String, Object> paramMap = (Map)jsonObject.get("parameters");
        Object result = null;
        for (Method method : mObject.getClass().getMethods()) {{
            if (methodName.equals(method.getName())) {{
                List<Object> paramList = new ArrayList<>();
                DefaultParameterNameDiscoverer parameterNameDiscoverer = new DefaultParameterNameDiscoverer();
                String[] names = parameterNameDiscoverer.getParameterNames(method);
                if (names != null) {{
                    for (String name : names) {{
                        paramList.add(paramMap.get(name));
                    }}
                }}
                try {{
                    result = method.invoke(mObject, paramList.toArray());
                }} catch (Exception e) {{
                    e.printStackTrace();
                }}
                break;
            }}
        }}
        return result;
    }}
}}
