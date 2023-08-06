workflows_schema_yaml = """type: object
additionalProperties: false
properties:
  workflows:
    type: array
    items:
      oneOf:
        - $ref: '#/components/schemas/workflow-template'
        - $ref: '#/components/schemas/workflow-no-template'
required:
  - workflows
components:
  schemas:
    workflow-template:
      type: object
      properties:
        name:
          type: string
          minLength: 1
        template:
          type: object
          additionalProperties: false
          properties:
            image:
              type: string
              minLength: 1
            commands:
              type: array
              items:
                type: string
                minLength: 1
              minItems: 1
            artifacts:
              type: array
              items:
                type: string
                minLength: 1
              minItems: 1
            resources:
              oneOf:
                - $ref: '#/components/schemas/resources'
          required:
            - image
            - commands
        depends-on:
          oneOf:
            - $ref: '#/components/schemas/depends-on-object'
            - $ref: '#/components/schemas/depends-on-array'
      additionalProperties: false
      required:
        - name
        - template
    workflow-no-template:
      type: object
      properties:
        name:
          type: string
          minLength: 1
        image:
          type: string
          minLength: 1
        commands:
          type: array
          items:
            type: string
            minLength: 1
          minItems: 1
        artifacts:
          type: array
          items:
            type: string
            minLength: 1
          minItems: 1
        resources:
          oneOf:
            - $ref: '#/components/schemas/resources'
        depends-on:
          oneOf:
            - $ref: '#/components/schemas/depends-on-object'
            - $ref: '#/components/schemas/depends-on-array'
      additionalProperties: false
      required:
        - name
        - image
        - commands
    depends-on-object:
      type: object
      additionalProperties: false
      properties:
        repo:
          type: object
          properties:
            include:
              type: array
              items:
                type: string
                minLength: 1
              minItems: 1
        workflows:
          type: array
          items:
            type: string
            minLength: 1
          minItems: 1
    depends-on-array:
      type: array
      items:
        type: string
        minLength: 1
      minItems: 1
    resources:
      type: object
      additionalProperties: false
      properties:
        cpu:
          type: object
          properties:
            count:
              type: integer
              minimum: 1
          required:
            - count
        memory:
          type: string
          minLength: 1
        gpu:
          type: object
          properties:
            count:
              type: integer
              minimum: 1
            name:
              type: string
              minLength: 1
            memory:
              type: string
              minLength: 1
          required:
            - count
      """