import json

def generate_zod_schema(schema_type, fields=None, item_type=None):
    if schema_type == "object" and fields:
        schema = "z.object({\n"
        for field_name, field_type in fields:
            schema += f"  {field_name}: z.{field_type}(),\n"
        schema += "})"
    elif schema_type == "array" and item_type:
        schema = f"z.array(z.{item_type}())"
    else:
        schema = f"z.{schema_type}()"
    
    return f"import {{ z }} from 'zod';\n\nconst schema = {schema};"

def generate_shadcn_form(form_name, fields, use_zod):
    form_fields = ""
    for field_name, field_type in fields:
        if field_type == "text":
            form_fields += f'''
  <FormField
    control={{{{form.control}}}}
    name="{field_name}"
    render={{{{ {{{{field}}}} => (
      <FormItem>
        <FormLabel>{field_name.capitalize()}</FormLabel>
        <FormControl>
          <Input {{{{...field}}}} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}}}}
  />
'''
        # Add more field types here...

    zod_import = "import { z } from 'zod';" if use_zod else ""
    zod_schema = f"""
const formSchema = z.object({{
  {", ".join([f"{name}: z.string()" for name, _ in fields])}
}})
""" if use_zod else ""

    return f"""import {{ useForm }} from 'react-hook-form'
import {{ Button }} from "@/components/ui/button"
import {{
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
}} from "@/components/ui/form"
import {{ Input }} from "@/components/ui/input"
{zod_import}

{zod_schema}

export function {form_name}() {{
  const form = useForm{f"<z.infer<typeof formSchema>>" if use_zod else ""}({{
    {f"resolver: zodResolver(formSchema)," if use_zod else ""}
    defaultValues: {{
      {", ".join([f"{name}: ''" for name, _ in fields])}
    }},
  }})

  function onSubmit(values) {{
    console.log(values)
  }}

  return (
    <Form {{...form}}>
      <form onSubmit={{form.handleSubmit(onSubmit)}} className="space-y-8">
        {form_fields}
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}}
"""

def generate_server_action(action_name, http_method, params, use_zod):
    params_list = ", ".join([f"{name}: {type}" for name, type in params])
    zod_schema = f"""
const inputSchema = z.object({{
  {", ".join([f"{name}: z.{type}()" for name, type in params])}
}})
""" if use_zod else ""

    validation_code = f"""
  const validatedInput = inputSchema.parse({{ {", ".join([name for name, _ in params])} }})
""" if use_zod else ""

    return f"""import {{ z }} from 'zod'

{zod_schema}

export async function {action_name}({params_list}) {{
  'use server'
{validation_code}
  // TODO: Implement your server-side logic here
  console.log('Received data:', {{ {", ".join([name for name, _ in params])} }})

  // Example response
  return {{ success: true, message: 'Data processed successfully' }}
}}
"""

def generate_safe_action_form(form_name, fields):
    # Generate Zod schema for form validation
    zod_schema = f"""
const formSchema = z.object({{
  {", ".join([f"{name}: z.string()" for name, _ in fields])}
}})
"""

    # Generate form fields
    form_fields = ""
    for field_name, field_type in fields:
        form_fields += f'''
        <FormField
          control={{{{form.control}}}}
          name="{field_name}"
          render={{{{ {{{{field}}}} => (
            <FormItem>
              <FormLabel>{field_name.capitalize()}</FormLabel>
              <FormControl>
                <Input {{{{...field}}}} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}}}}
        />
'''

    # Generate the complete component with both client and server-side code
    return f"""'use client'

import {{ z }} from 'zod'
import {{ useForm }} from 'react-hook-form'
import {{ zodResolver }} from '@hookform/resolvers/zod'
import {{ createSafeAction }} from 'next-safe-action'
import {{
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
}} from '@/components/ui/form'
import {{ Input }} from '@/components/ui/input'
import {{ Button }} from '@/components/ui/button'
import {{ useAction }} from 'next-safe-action/hook'

{zod_schema}

const action = createSafeAction(formSchema, async (data) => {{
  // TODO: Implement your server-side logic here
  console.log('Received data:', data)
  return {{ message: 'Form submitted successfully' }}
}})

export function {form_name}() {{
  const form = useForm<z.infer<typeof formSchema>>({{
    resolver: zodResolver(formSchema),
    defaultValues: {{
      {", ".join([f"{name}: ''" for name, _ in fields])}
    }},
  }})

  const {{ execute, result, status }} = useAction(action)

  const onSubmit = (values: z.infer<typeof formSchema>) => {{
    execute(values)
  }}

  return (
    <Form {{...form}}>
      <form onSubmit={{form.handleSubmit(onSubmit)}} className="space-y-8">
        {form_fields}
        <Button type="submit" disabled={{{{status === 'executing'}}}}>
          {{{{status === 'executing' ? 'Submitting...' : 'Submit'}}}}
        </Button>
        {{{{result && result.data && (
          <p className="mt-4 text-green-600">{{{{result.data.message}}}}</p>
        )}}}}
      </form>
    </Form>
  )
}}
"""